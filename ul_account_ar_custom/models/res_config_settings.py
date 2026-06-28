from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    no_backorder = fields.Boolean(
        string='No Backorder on Partial Validation',
        related='company_id.no_backorder',
        readonly=False,
    )
