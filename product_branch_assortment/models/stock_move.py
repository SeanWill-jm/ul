from odoo import api, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.constrains("product_id", "location_id", "location_dest_id", "company_id", "origin_returned_move_id")
    def _check_branch_assortment(self):
        """Refuse stock entering a branch that is not allowed to stock the product.

        Checked: receipts, inbound inter-branch transfers, positive inventory
        adjustments (any move whose destination is an internal location of a
        non-allowed branch).

        Not checked (sell-down and operational safety):
        - outgoing moves (deliveries, negative adjustments, scrap);
        - internal relocations inside the same branch;
        - customer returns (``origin_returned_move_id`` set).
        """
        for move in self:
            dest = move.location_dest_id
            if dest.usage != "internal" or move.origin_returned_move_id:
                continue
            company = dest.company_id or move.company_id
            if not company:
                continue
            source = move.location_id
            if source.usage == "internal" and (source.company_id or move.company_id) == company:
                continue
            if move.product_id._is_allowed_for_company(company):
                continue
            raise ValidationError(move.product_id._branch_assortment_error(company))
