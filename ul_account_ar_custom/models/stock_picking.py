from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from itertools import groupby
import pandas as pd


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if self.env.company.no_backorder and not self.env.context.get('skip_backorder'):
            return super().with_context(
                skip_backorder=True,
                picking_ids_not_to_backorder=self.ids,
            ).button_validate()
        return super().button_validate()

    @api.model
    def _create_picking_from_pos_order_lines(self, location_dest_id, lines, picking_type, partner=False):
        """Override to keep POS-created pickings in draft state instead of auto-validating."""
        pickings = self.env['stock.picking']
        stockable_lines = lines.filtered(
            lambda l: l.product_id.type == 'consu' and not l.product_id.uom_id.is_zero(l.qty))
        if not stockable_lines:
            return pickings
        positive_lines = stockable_lines.filtered(lambda l: l.qty > 0)
        negative_lines = stockable_lines - positive_lines

        if positive_lines:
            location_id = picking_type.default_location_src_id.id
            positive_picking = self.env['stock.picking'].create(
                self._prepare_picking_vals(partner, picking_type, location_id, location_dest_id)
            )
            positive_picking._create_move_from_pos_order_lines(positive_lines)
            # Do NOT call _action_done() — leave picking in draft/confirmed state
            pickings |= positive_picking

        if negative_lines:
            if picking_type.return_picking_type_id:
                return_picking_type = picking_type.return_picking_type_id
                return_location_id = return_picking_type.default_location_dest_id.id
            else:
                return_picking_type = picking_type
                return_location_id = picking_type.default_location_src_id.id

            negative_picking = self.env['stock.picking'].create(
                self._prepare_picking_vals(partner, return_picking_type, location_dest_id, return_location_id)
            )
            negative_picking._create_move_from_pos_order_lines(negative_lines)
            # Do NOT call _action_done() — leave picking in draft/confirmed state
            pickings |= negative_picking

        return pickings