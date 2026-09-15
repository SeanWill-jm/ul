from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    warehouse_delivery_address_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Address",
        related="picking_type_id.warehouse_id.partner_id",
        readonly=True,
        help=(
            "Address of the warehouse selected by the standard Deliver To field. "
            "This field is informational and is printed on the RFQ/Purchase Order. "
            "Change Deliver To to select a different receiving warehouse."
        ),
    )
