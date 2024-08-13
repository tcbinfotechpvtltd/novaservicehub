from odoo import fields, models, api


class HrExpenses(models.Model):
    _inherit = 'hr.expense'

    master_id = fields.Many2one('expense.master', string='Expense Master')

    @api.onchange('master_id')
    def _onchange_master_id(self):
        if self.master_id:
            self.project_name = self.master_id.project_id.id


class HeExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    master_id = fields.Many2one('expense.master', string='Expense Master')
