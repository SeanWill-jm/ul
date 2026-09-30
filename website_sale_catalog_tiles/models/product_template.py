from odoo import models
from odoo.tools import float_round


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _tile_on_hand_info(self, variant, website):
        """Return what the shop tile needs to render availability.

        Uses the same source as the standard product page (website_sale_stock):
        the quantity available in the website's warehouse, read under ``sudo()``
        because public/portal visitors have no access to stock quants. Read-only,
        one variant, rounded down to a whole unit, so nothing sensitive leaks
        beyond the number the standard product page already shows when "Show
        availability Qty" is enabled.

        :return: dict(is_storable, free_qty, allow_out_of_stock)
        """
        self.ensure_one()
        if not self.is_storable or not variant:
            return {"is_storable": False, "free_qty": 0, "allow_out_of_stock": True}
        variant_sudo = variant.sudo()
        qty = website.sudo()._get_product_available_qty(variant_sudo)
        return {
            "is_storable": True,
            "free_qty": float_round(qty, precision_digits=0, rounding_method="DOWN"),
            "allow_out_of_stock": variant_sudo.allow_out_of_stock_order,
        }
