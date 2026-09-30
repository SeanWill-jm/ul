# Implementation Specification (19.0.1.0.1)

## In scope

- Odoo.sh 19.0, Purchase + Inventory (`purchase_stock`).
- Editable Delivery Address chosen from contacts tagged `PO Delivery Address`.
- Printed on RFQ and PO PDFs (extra block), vendor portal, list column/search/group-by.

## Out of scope

- Deliver To, Dropship Address, receipt/picking changes.
- Email template body changes (attached PDF carries the address).
- New destination master model; creation of contacts from the dropdown.

## Field

| Attribute | Value |
|---|---|
| Model | `purchase.order` |
| Field | `po_delivery_address_id` |
| Label | Delivery Address |
| Type | Many2one `res.partner` |
| Stored | Yes (btree_not_null index) |
| Editable | Yes, all states |
| Tracking | Yes |
| Copy | Yes |
| ondelete | restrict |
| Domain | `category_id in [PO Delivery Address tag]` (callable) |
| Constraint | selected contact must carry the tag (checked when the field is written) |

## Tag

`res.partner.category` "PO Delivery Address", XML ID
`purchase_warehouse_delivery_address.partner_category_po_delivery_address`, noupdate.

## Report conditions (1.0.4)

- Delivery Address block prints when `o.po_delivery_address_id` is set (name, address, phone). Empty -> standard document.
- Standard Shipping address (`dest_address_id`) prints only when `dest_address_id` is set **and** no Delivery Address is chosen.
- Vendor block: name, address, phone via the contact widget (without `vat`), then `TAX ID: <res.partner.vat>` when the vendor has one.
- RFQ template: Requested Ship Date (`date_planned`) prints inside the Delivery Address block because the hidden standard block carried it.
- Both templates: `purchase.report_purchaseorder_document`, `purchase.report_purchasequotation_document`.

## Failure behaviour

Tag deleted -> dropdown empty and writes of the field raise a clear ValidationError.
Tag removed from a contact later -> existing orders keep printing it; unrelated edits are not
blocked.
