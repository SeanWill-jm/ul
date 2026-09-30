# Changelog

## 19.0.1.0.4

Report layout (client request): standard Shipping address hidden only when a Delivery Address is set;
vendor tax number relabelled `TAX ID:` on both RFQ and PO templates; RFQ Requested Ship Date kept.
See PATCH_NOTES_19.0.1.0.4.md.

## 19.0.1.0.3

Tests only: test 08 no longer uses the non-existent `done` state (19.0 selection has no `done`; it uses
`locked`). States are read from the field and each is tested locked and unlocked. No functional change.

## 19.0.1.0.2

Fix: search view Group By `<group>` no longer carries a `string` attribute (rejected by the
19.0 search view schema on Staging). No functional change. See PATCH_NOTES_19.0.1.0.2.md.

## 19.0.1.0.1

Concept change: the Delivery Address is now a user-selected, tagged contact.

### Added
- `purchase.order.po_delivery_address_id` (Delivery Address), editable, tracked.
- Contact tag `PO Delivery Address` (noupdate data) driving the dropdown; write-time constraint.
- Extra Delivery Address block on RFQ and PO PDFs (both report templates) and on the portal.
- Optional list column, search field and Group By.

### Removed
- `warehouse_delivery_address_id` and the warehouse-derived read-only display/print block.

## 19.0.1.0.0

Initial release: read-only Delivery Address derived from Deliver To warehouse.
