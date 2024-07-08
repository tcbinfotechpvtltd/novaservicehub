from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_name = fields.Many2one('project.project',string="Project Name")
    site = fields.Char(string="Site")
    description = fields.Html(string="Description")

    @api.onchange('project_name')
    def _onchange_project_name(self):
        if self.project_name and self.project_name.partner_id:
            self.partner_id = self.project_name.partner_id.id

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if res.project_name:
            res.project_name.partner_id = res.partner_id
        return res

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if 'project_name' in vals:
            for order in self:
                if order.project_name:
                    order.project_name.partner_id = order.partner_id
        return res

