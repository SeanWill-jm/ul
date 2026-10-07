from odoo import api, models
from odoo.tools import float_compare


class ProductProduct(models.Model):
    """``product.product`` delegates its fields to ``product.template`` through
    ``_inherits``; ``allowed_branch_ids`` is therefore already readable, writable
    and searchable on variants. Only the helper methods need forwarding."""

    _inherit = "product.product"

    def _is_allowed_for_company(self, company):
        self.ensure_one()
        return self.product_tmpl_id._is_allowed_for_company(company)

    @api.model
    def _branch_assortment_domain(self, company):
        return self.env["product.template"]._branch_assortment_domain(company)

    def _branch_assortment_error(self, company):
        self.ensure_one()
        return self.product_tmpl_id._branch_assortment_error(company)

    def _has_branch_stock(self, company):
        """True when ``company`` still holds on-hand stock of this variant.

        Used for the agreed sell-down rule: a branch removed from a product's
        assortment may keep selling what it already has.

        ``sudo()`` is deliberate and minimal: a read-only aggregate on quants of
        the given company only, so the check does not depend on which companies
        the writing user currently has enabled in the company switcher.
        """
        self.ensure_one()
        if not company or not self.is_storable:
            return False
        rows = self.env["stock.quant"].sudo()._read_group(
            [
                ("product_id", "=", self.id),
                ("company_id", "=", company.id),
                ("location_id.usage", "=", "internal"),
            ],
            aggregates=["quantity:sum"],
        )
        quantity = (rows[0][0] if rows else 0.0) or 0.0
        return float_compare(quantity, 0.0, precision_rounding=self.uom_id.rounding) > 0
