# Deployment Plan (19.0.1.0.1)

## Staging (1.0.0 already installed)

1. Copy the new `purchase_warehouse_delivery_address/` over the existing folder in
   `~/src/user/` (files are live in the online editor, the schema is not).
2. Upgrade: `odoo-bin -d $PGDATABASE -u purchase_warehouse_delivery_address --stop-after-init`
   then `odoosh-restart http`.
3. Optionally run the module tests, then tag the delivery contacts and run the UAT cases.
4. Commit and push: `git push https HEAD:test`.

## Production

Only after UAT sign-off: confirm a current backup, merge the approved revision, wait for the
build, upgrade the module, tag the production contacts, print one RFQ and one PO to compare
with Staging.

## Post-deployment

Verify RFQ/PO printing, dropship POs, Deliver To, receipt creation and the vendor portal page.
