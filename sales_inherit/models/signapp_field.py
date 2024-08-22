from odoo import models,fields,api


class SignappField(models.Model):
    _inherit = 'signapp.field'


    late_fee_amount = fields.Char("Late - Fee - Amount")
