from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_state_id = fields.Many2one(
        'res.country.state',
        related='partner_id.state_id',
        string='Partner State',
        store=True,
    )
