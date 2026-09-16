from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import unquote


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # ------------------------------------------------------------------
    # UI convenience: the product pickers on the order line only propose
    # products in the assortment of the order's company. ``product_template_id``
    # reuses the ``product_id`` domain through ``_description_domain`` in
    # standard 19.0, so one override covers both pickers.
    # ------------------------------------------------------------------
    def _domain_product_id(self):
        domain = super()._domain_product_id()
        return domain + self.env["product.product"]._branch_assortment_domain(
            unquote("company_id")
        )

    # ------------------------------------------------------------------
    # Integrity: imports, RPC and edited views cannot bypass the assortment.
    # Sell-down rule: a branch that still holds stock of the product may sell it.
    # ------------------------------------------------------------------
    @api.constrains("product_id", "company_id")
    def _check_branch_assortment(self):
        for line in self:
            product = line.product_id
            company = line.company_id
            if not product or line.display_type or not company:
                continue
            if product._is_allowed_for_company(company):
                continue
            if product._has_branch_stock(company):
                continue
            raise ValidationError(product._branch_assortment_error(company))
