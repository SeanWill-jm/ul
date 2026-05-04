from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    ul_location = fields.Char(string='Location', copy=False)
    ul_ship_via = fields.Char(string='Ship Via', copy=False)
    ul_account_no = fields.Char(string='Account No', copy=False)
    ul_other_info = fields.Char(string='Other Info', copy=False)
