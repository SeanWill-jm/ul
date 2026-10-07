from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

PO_DELIVERY_TAG_XMLID = (
    "purchase_warehouse_delivery_address.partner_category_po_delivery_address"
)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    po_delivery_address_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Address",
        domain=lambda self: self._po_delivery_address_domain(),
        tracking=True,
        copy=True,
        index="btree_not_null",
        ondelete="restrict",
        help=(
            "Contact printed as the Delivery Address on the RFQ / Purchase Order. "
            "Only contacts tagged 'PO Delivery Address' can be selected, one at a time. "
            "This is separate from Deliver To (the receiving operation) and from the "
            "Dropship Address. Leave empty to print the standard document."
        ),
    )

    @api.model
    def _po_delivery_address_tag(self):
        """Return the 'PO Delivery Address' tag (empty recordset if it was deleted)."""
        return self.env.ref(PO_DELIVERY_TAG_XMLID, raise_if_not_found=False) or (
            self.env["res.partner.category"]
        )

    @api.model
    def _po_delivery_address_domain(self):
        tag = self._po_delivery_address_tag()
        if not tag:
            # Tag missing -> nothing selectable; the constraint reports the cause.
            return [("id", "=", False)]
        return [("category_id", "in", tag.ids)]

    @api.constrains("po_delivery_address_id")
    def _check_po_delivery_address_tag(self):
        """The dropdown domain is client-side only; enforce the tag on write/import.

        Fires only when the field itself is written, so removing the tag from a
        contact later never blocks unrelated edits of existing orders.
        """
        orders = self.filtered("po_delivery_address_id")
        if not orders:
            return
        tag = self._po_delivery_address_tag()
        if not tag:
            raise ValidationError(_(
                "The contact tag 'PO Delivery Address' no longer exists. "
                "Recreate it or restore the module data before choosing a Delivery Address."
            ))
        for order in orders:
            # Read-only tag check, sudo so a narrowed company switcher cannot hide the tag.
            if tag not in order.po_delivery_address_id.sudo().category_id:
                raise ValidationError(_(
                    "Contact '%(name)s' cannot be used as Delivery Address because it "
                    "does not carry the tag '%(tag)s'. Add the tag on the contact first.",
                    name=order.po_delivery_address_id.display_name,
                    tag=tag.name,
                ))
