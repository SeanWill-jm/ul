# Patch notes — 19.0.1.0.1

**Type:** functional change (concept change requested by Thomas, 2026-09-30).
**Runtime validation status:** Python syntax validated, XML well-formedness validated,
ZIP integrity validated. Runtime installation/upgrade and the test suite are **not yet
validated** — run them on Odoo.sh Staging first.

## What changed

- **Removed** `warehouse_delivery_address_id` (non-stored related field, warehouse address
  derived from Deliver To) and its read-only display and printed block.
- **Added** `purchase.order.po_delivery_address_id` — label **Delivery Address**, stored
  Many2one to `res.partner`, tracked in chatter, copied on duplicate, editable in every state.
- **Added** contact tag **PO Delivery Address** (`res.partner.category`, noupdate data).
  The dropdown domain is that tag; a constraint enforces it on write/import.
- **Form:** field placed in the left column under Currency (structural anchor
  `//sheet/group/group[1]`); no "create" from the dropdown.
- **Lists/search:** optional hidden column on the RFQ and PO lists, search field, Group By.
- **Reports:** extra "Delivery Address" block (name, address, phone) on
  `purchase.report_purchaseorder_document` **and** `purchase.report_purchasequotation_document`
  (1.0.0 only covered the first). Standard "Shipping address" (Dropship) is untouched.
- **Portal:** "Delivery Address" row on the vendor portal PO/RFQ page.
- Tests rewritten (14).

## What did not change

- Technical name, dependency (`purchase_stock`), Deliver To, Dropship Address, receipt
  creation, email templates (the attached PDF carries the address).

## Upgrade notes (1.0.0 was installed on staging)

- XML IDs of the form view and the PO report template are reused, so the upgrade replaces the
  1.0.0 records in place.
- The old field was non-stored: no column is dropped and no PO data is lost.
- Existing POs have an empty Delivery Address after the upgrade and print as standard.
- Run: `odoo-bin -d $PGDATABASE -u purchase_warehouse_delivery_address --stop-after-init`,
  then `odoosh-restart http`.

## Known risks (unvalidated at runtime)

- XPath anchors verified against 19.0 source text only; staging customisations (the form shows
  custom fields such as Account No / Ship Via) could change the resolved view.
- Test 08 writes `state` directly; test 11–13 use `ir.actions.report._render_qweb_html`.
  Adjust if the 19.0 runtime API differs.
