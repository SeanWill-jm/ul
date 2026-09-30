# Rollback Plan (19.0.1.0.1)

The module adds one stored Many2one column (`purchase_order.po_delivery_address_id`), one
contact tag, and inherited views/report templates/portal template.

If a problem occurs on Staging:

1. Stop further changes and read the Odoo.sh logs.
2. Redeploy the 1.0.0 folder over `~/src/user/purchase_warehouse_delivery_address` and run
   `-u purchase_warehouse_delivery_address`. The 1.0.0 field is a non-stored related field, so
   nothing needs migrating back. Delivery Addresses chosen under 1.0.1 are then no longer
   shown or printed; the column data is left in place until the module is uninstalled.
3. Verify the standard Purchase form and the RFQ/PO PDFs.

Do not delete the tag record while orders still use it. Contact data is never modified by the
module.
