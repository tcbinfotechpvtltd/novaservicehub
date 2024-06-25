from odoo import fields, models, api


class HrExpenses(models.Model):
    _inherit = 'product.product'

    project_id = fields.Many2one('project.project', string="Project Name")