from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    ul_account_no = fields.Char(string='Account No', copy=False)
    ul_ship_via = fields.Char(string='Ship Via', copy=False)
