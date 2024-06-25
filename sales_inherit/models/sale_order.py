from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_name = fields.Many2one('project.project',string="Project Name")




