from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    tile_show_reference = fields.Boolean(
        string="Show Internal Reference on Tiles",
        default=True,
        help="Show the product's internal reference (SKU) on each shop tile.",
    )
    tile_show_on_hand = fields.Selection(
        selection=[
            ("none", "Never"),
            ("logged", "Logged-in customers only"),
            ("all", "Everyone"),
        ],
        string="Show On-Hand Quantity on Tiles",
        default="logged",
        required=True,
        help="Show the quantity available in the website's warehouse on each shop "
        "tile. 'Logged-in customers only' suits wholesale sites with accounts "
        "on invitation.",
    )
    tile_quantity_picker = fields.Boolean(
        string="Quantity Picker on Tiles",
        default=True,
        help="Show a quantity field with -/+ buttons next to Add to Cart on each "
        "shop tile; the chosen quantity is added in one click.",
    )

    def _tile_can_show_on_hand(self):
        """Whether the on-hand quantity may be rendered for the current visitor."""
        self.ensure_one()
        if self.tile_show_on_hand == "all":
            return True
        if self.tile_show_on_hand == "logged":
            return not self.env.user._is_public()
        return False
