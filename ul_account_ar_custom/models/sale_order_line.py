from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_delivered_method = fields.Selection(
        selection_add=[('pick_move', 'Pick Moves (2-Step)')]
    )

    @api.depends('product_id')
    def _compute_qty_delivered_method(self):
        super()._compute_qty_delivered_method()
        for line in self:
            if not line.is_expense and line.product_id.invoice_policy == 'picking' and line.product_id.type == 'consu':
                line.qty_delivered_method = 'pick_move'

    def _prepare_qty_delivered(self):
        delivered_qties = super()._prepare_qty_delivered()
        for line in self.filtered(lambda l: l.qty_delivered_method == 'pick_move'):
            qty = 0.0
            warehouse = line.order_id.warehouse_id
            pick_type = warehouse.pick_type_id if warehouse.delivery_steps == 'pick_ship' else False

            for move in line.move_ids:
                if move.state != 'done':

                    continue
                # Count moves that belong to the pick operation type (internal pick step)
                if pick_type and move.picking_id.picking_type_id == pick_type:
                    qty += move.product_uom._compute_quantity(
                        move.quantity, line.product_uom_id, rounding_method='HALF-UP'
                    )
                # Also count direct outgoing moves (1-step or ship step already done)
                elif move.location_dest_id._is_outgoing():
                    if not move.origin_returned_move_id or move.to_refund:
                        qty += move.product_uom._compute_quantity(
                            move.quantity, line.product_uom_id, rounding_method='HALF-UP'
                        )

            delivered_qties[line] = qty
        return delivered_qties

    # no trigger product_id.invoice_policy to avoid retroactively changing SO
    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'state')
    def _compute_qty_to_invoice(self):
        super()._compute_qty_to_invoice()
        for line in self:
            if line.state == 'sale' and not line.display_type and line.product_id.invoice_policy == 'picking':
                line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
