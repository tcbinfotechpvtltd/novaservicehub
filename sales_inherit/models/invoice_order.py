from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'


    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order", compute='_compute_sale_order_id',store=True)
    project_id = fields.Many2one('project.project', string="Project Name",related="sale_order_id.project_name")


    @ api.depends('invoice_line_ids.sale_line_ids.order_id')
    def _compute_sale_order_id(self):
        for rec in self:
            rec.sale_order_id = rec.mapped('invoice_line_ids.sale_line_ids.order_id')[:1]
