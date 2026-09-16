from odoo import api, models
from odoo.exceptions import ValidationError


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.constrains("product_id", "warehouse_id", "company_id")
    def _check_branch_assortment(self):
        for orderpoint in self:
            company = orderpoint.warehouse_id.company_id or orderpoint.company_id
            if not company or orderpoint.product_id._is_allowed_for_company(company):
                continue
            raise ValidationError(orderpoint.product_id._branch_assortment_error(company))

    def _get_orderpoint_products(self):
        """Keep the Replenishment report from proposing products outside the
        current company's assortment (it creates manual orderpoints, which the
        constraint above would otherwise refuse and break the report)."""
        products = super()._get_orderpoint_products()
        company = self.env.company
        if not company.parent_id:
            return products
        if not products:
            return products
        return products.search(
            [("id", "in", products.ids)] + products._branch_assortment_domain(company)
        )
