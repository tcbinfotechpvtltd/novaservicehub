from odoo import fields, models, api


class HrExpenses(models.Model):
    _inherit = 'project.project'

    sale_id = fields.One2many('sale.order', 'project_name', string='Sale')
    invoicing_id = fields.One2many('account.move', 'project_id', string='Invoicing')
    expense_id = fields.One2many('hr.expense', 'project_name', string='Expense')
    profit_loss = fields.Float(string='Settled Profit & Loss', compute='_compute_profit_loss')
    unsettled_profit_loss = fields.Float(string='Unsettled Profit & Loss', compute='_compute_profit_loss')

    allow_billable = fields.Boolean(default=True)




    @api.depends('invoicing_id.state', 'sale_id.state', 'expense_id.state')
    def _compute_profit_loss(self):
        for project in self:
            invoicing_total = 0.0
            expense_total = 0.0
            unsettled_invoicing_total = 0.0
            unsettled_expense_total = 0.0
            # if all([
            #     project.invoicing_id,
            #     project.sale_id.filtered(lambda sale: sale.state in ['sale', 'done']),
            #     project.expense_id
            # ]):
            invoicing_total = sum(
                project.invoicing_id.filtered(lambda inv: inv.payment_state == 'paid').mapped('amount_total'))
            expense_total = sum(
                project.expense_id.filtered(lambda exp: exp.state == 'done').mapped('total_amount'))
            unsettled_invoicing_total = sum(
                project.invoicing_id.filtered(lambda exp: exp.state !='cancel').mapped('amount_total'))
            unsettled_expense_total = sum(
                project.expense_id.filtered(lambda exp: exp.state !='refused').mapped('total_amount'))
            project.profit_loss = invoicing_total - expense_total 
            project.unsettled_profit_loss = unsettled_invoicing_total - unsettled_expense_total


    def invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Orders',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('project_name', '=', self.id)],  # You can add a domain if you want to filter the records
            # 'context': {'create': False},  # You can customize the context if needed
        }

    def view_expenses(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expense',
            'view_mode': 'tree,form',
            'res_model': 'hr.expense',
            'domain': [('project_name', '=', self.id)],  # You can add a domain if you want to filter the records
            # 'context': {'create': False},  # You can customize the context if needed
        }

    def view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('project_id', '=', self.id)],  # You can add a domain if you want to filter the records
            # 'context': {'create': False},  # You can customize the context if needed
        }


