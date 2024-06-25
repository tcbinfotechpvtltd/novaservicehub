from odoo import fields, models, api


class HrExpenses(models.Model):
    _inherit = 'hr.expense'

    project_name = fields.Many2one('project.project',string="Project Name")
