from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ExpenseMaster(models.Model):
    _name = 'expense.master'
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin', 'analytic.mixin']
    _description = 'Expense Master'
    _order = "id desc"

    name = fields.Char(string='Expense Name', required=True)
    expense_ids = fields.One2many('hr.expense', 'master_id', string='Expenses')
    sheet_ids = fields.One2many('hr.expense.sheet', 'master_id')
    nb_expense = fields.Integer(compute='_compute_nb_expense', string="Number of Expenses")
    nb_report = fields.Integer(compute='_compute_nb_report', string="Number of Reports")
    nb_attachment = fields.Integer(string="Number of Attachments", compute='_compute_nb_attachment')
    is_submitted = fields.Boolean(string="Submitted")
    is_approved = fields.Boolean(string="Approved")
    is_post_entries = fields.Boolean(string="Post Journal Entries")
    is_payment = fields.Boolean(string="Payment")
    project_id = fields.Many2one('project.project',string="Project Name")

    @api.onchange('project_id')
    def _onchange_master_id(self):
        for rec in self.expense_ids:
            rec.project_name = self.project_id.id

    @api.depends('expense_ids')
    def _compute_nb_expense(self):
        for sheet in self:
            sheet.nb_expense = len(sheet.expense_ids)

    @api.depends('sheet_ids')
    def _compute_nb_report(self):
        for sheet in self:
            sheet.nb_report = len(sheet.sheet_ids)

    def _compute_nb_attachment(self):
        attachment_data = self.env['ir.attachment']._read_group(
            [('res_model', '=', 'expense.master'), ('res_id', 'in', self.ids)],
            ['res_id'],
            ['__count'],
        )
        attachment = dict(attachment_data)
        for expense in self:
            expense.nb_attachment = attachment.get(expense._origin.id, 0)

    def action_submit_expenses(self):
        for rec in self.expense_ids:
            if rec.filtered(lambda expense: not expense.is_editable):
                raise UserError(_('You are not authorized to edit this expense.'))
            sheet_id = self.env['hr.expense.sheet'].create(rec._get_default_expense_sheet_values())
            sheet_id.master_id = self.id


    def action_submit_sheet(self):
        for rec in self.sheet_ids:
            rec.action_submit_sheet()
        self.is_submitted = True

    def action_approve_expense_sheets(self):
        for rec in self.sheet_ids:
            rec.action_approve_expense_sheets()
        self.is_approved = True

    def action_sheet_move_create(self):
        for rec in self.sheet_ids:
            rec.action_sheet_move_create()
        self.is_post_entries = True        

    def action_register_payment(self):
        payment_method = self.env.ref('account.account_payment_method_manual_out')
        journal_id = self.env['account.journal'].search([('name', '=', 'Bank')], limit=1) 
        print("\n\n\n\n\njournalllllllll", journal_id, payment_method)
        for rec in self.sheet_ids:
            print("\n\n\n\n\n\n\n\naccount_move_ids", rec.account_move_ids)
            for move in rec.account_move_ids:
                print("\n\n\n\n\n\n\nreccccccc", move.payment_ids)
                payment_vals = {
                    'partner_id': rec.employee_id.user_partner_id.id,
                    'amount': move.amount_total,
                    'payment_type': 'outbound',  # Assuming payment to employee
                    'partner_type': 'supplier',  # Treat employee as a supplier
                    'payment_method_line_id': payment_method.id,
                    'journal_id': journal_id.id if journal_id else move.journal_id.id,
                    'date': fields.Date.today(),
                    'ref': rec.name,
                    'payment_reference': rec.name,  # Link payment to the sheet
                }
                
                # Create the payment
                payment = self.env['account.payment'].create(payment_vals)
                payment.move_id = move.id
                # Post the payment
                payment.action_post()
                print("\n\n\n\n\n\n\npaymenttttttttttttttt", payment)
            rec.write({'state': 'done'})
        is_payment = True

    def action_open_expense_view(self):
        self.ensure_one()
        if self.nb_expense == 1:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'hr.expense',
                'res_id': self.expense_ids.id,
            }
        return {
            'name': _('Expenses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'views': [[False, "list"], [False, "form"]],
            'res_model': 'hr.expense',
            'domain': [('id', 'in', self.expense_ids.ids)],
        }

    def action_open_report_view(self):
        self.ensure_one()
        if self.nb_report == 1:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'hr.expense.sheet',
                'res_id': self.sheet_ids.id,
            }
        return {
            'name': _('Reports'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'views': [[False, "list"], [False, "form"]],
            'res_model': 'hr.expense.sheet',
            'domain': [('id', 'in', self.sheet_ids.ids)],
        }

