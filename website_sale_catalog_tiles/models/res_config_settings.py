from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    tile_show_reference = fields.Boolean(
        related="website_id.tile_show_reference", readonly=False
    )
    tile_show_on_hand = fields.Selection(
        related="website_id.tile_show_on_hand", readonly=False
    )
    tile_quantity_picker = fields.Boolean(
        related="website_id.tile_quantity_picker", readonly=False
    )
