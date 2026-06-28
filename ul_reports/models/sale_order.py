from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ul_account_no = fields.Char(string='Account No', copy=False)
    ul_location = fields.Char(string='Location', copy=False)
    ul_ship_via = fields.Char(string='Ship Via', copy=False)
