# Patch notes — 19.0.1.0.4

**Type:** client-requested change to the printed RFQ and Purchase Order (report layout only).
**Runtime validation status:** Python syntax, XML well-formedness, ZIP integrity validated.
Upgrade, the 17 tests and on-screen UAT on Staging are **not yet validated** for this version.
(1.0.3: upgrade + 14/14 tests passed on Staging 2026-09-30.)

## Client request and decisions (Thomas, 2026-09-30)

1. The standard "Shipping address" block on the left must go -> **hidden only when a Delivery
   Address is chosen**; with no Delivery Address the standard block still prints (dropship POs keep
   their customer address).
2. Delivery Address **stays in its current position** (row at the top of the page body).
3. The vendor tax number label `VAT:` becomes **`TAX ID:`** (for every vendor).
4. Vendor block keeps **name, address, phone, tax number**.

## Changes (both 19.0 templates: `report_purchaseorder_document` and `report_purchasequotation_document`)

- `t t-if="o.dest_address_id"` (standard Shipping address) -> `o.dest_address_id and not o.po_delivery_address_id`.
- Vendor block: `t-options` of the `o.partner_id` contact widget no longer lists `vat`; a separate
  `TAX ID: <vat>` line follows it (`res.partner.vat` itself is unchanged).
- RFQ template only: the standard shipping block also printed **Requested Ship Date**; when that
  block is hidden, the date now prints inside the Delivery Address block so it is not lost.
- Tests 15-17 (tax label printed once, no tax line without a VAT, shipping block hidden only when a
  Delivery Address is set; both report templates).

## What did not change

Model, tag, constraint, form/list/search views, portal, Deliver To, Dropship field, receipts,
global tax label (`vat_label`) and other companies' reports (invoices, quotations, sales orders).

## Notes and risks (unvalidated at runtime)

- Anchors (`//t[@t-if='o.dest_address_id']`, `//t[@t-set='address']/div[@t-field='o.partner_id']`)
  come from the 19.0 source text, read through a summarising fetch; runtime is authoritative.
- The "TAX ID" label is printed for foreign vendors too (their numbers are EIN/VAT, not TRN); the
  wording was chosen neutral for that reason.
- Test 15 creates a vendor with `no_vat_validation=True`; if `base_vat` uses a different context
  key in 19.0 the test may need adjusting.
- The standard `VAT` wording printed by the contact widget came from the widget itself; we
  replace it only on the RFQ/PO documents, not globally.
- Requested Ship Date in the RFQ branch is not asserted by an automated test (date_planned is
  computed from lines); it is covered by UAT.
