# Architecture (19.0.1.0.1)

## Business requirement

The buyer chooses one delivery contact from a controlled list. That contact is printed as the
Delivery Address on the RFQ and the Purchase Order, and shown to the vendor on the portal.

## Design decision

A dedicated stored Many2one, `purchase.order.po_delivery_address_id`, driven by a contact tag.
It is **independent** of:

- **Deliver To** (`picking_type_id`) — the operation used to create the receipt;
- **Dropship Address** (`dest_address_id`) — standard direct-to-customer delivery.

The 1.0.0 design (one source of truth = Deliver To warehouse) was replaced on request. The
consequence is that the printed address can differ from the receiving warehouse; that is now a
buyer decision, not a system guarantee.

## Data flow

```text
Contact form: tag "PO Delivery Address"
  -> dropdown domain (client side) + constraint (server side)
  -> purchase.order.po_delivery_address_id
  -> RFQ PDF, PO PDF, vendor portal, list column / search / group by
```

## Reports (19.0 source)

Two templates exist and both are inherited:
`purchase.report_purchaseorder_document` (action `action_report_purchase_order`, RFQ or PO by
state) and `purchase.report_purchasequotation_document` (action `report_purchase_quotation`).
The block is inserted after the first `oe_structure` inside `div.page`. The standard
"Shipping address" block (`t t-if="o.dest_address_id"` + `information_block`) is hidden only when a Delivery Address is set (1.0.4). The vendor block (`t t-set="address"`) keeps the contact widget without `vat`, followed by a `TAX ID:` line; `res.partner.vat` and the global company tax label are not changed.

## Upgradeability

Only inherits standard models, views, templates. No core code is overridden. No `sudo()` except
one read-only tag check inside the constraint.
