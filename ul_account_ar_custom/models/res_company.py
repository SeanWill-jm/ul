from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    no_backorder = fields.Boolean(
        string='No Backorder on Partial Validation',
        default=False,
    )
