from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'


    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order", compute='_compute_sale_order_id',store=True)
    project_id = fields.Many2one('project.project', string="Project Name",related="sale_order_id.project_name")
    site = fields.Char(string="Site")
    description = fields.Html(string="Description")


    @ api.depends('invoice_line_ids.sale_line_ids.order_id')
    def _compute_sale_order_id(self):
        for rec in self:
            rec.sale_order_id = rec.mapped('invoice_line_ids.sale_line_ids.order_id')[:1]

    @api.model
    def create(self, vals):
        if 'invoice_origin' in vals and vals['invoice_origin']:
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
            if sale_order:
                vals.update({
                    'site': sale_order.site,
                    'description': sale_order.description,
                })
        return super(AccountMove, self).create(vals)
