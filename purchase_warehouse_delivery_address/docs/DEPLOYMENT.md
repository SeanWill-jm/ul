# Deployment Plan

## Development

Push the module, confirm a green build, update the Apps list, install, and perform initial testing.

## Staging

Use a production-data staging copy. Verify real warehouse addresses, execute all UAT cases, and obtain business approval.

## Production

1. Confirm current Odoo.sh backup.
2. Merge the approved Git revision.
3. Wait for successful build.
4. Install/upgrade the module.
5. Validate one known PO for each receiving warehouse.
6. Print sample PDFs and compare with Staging.

## Post-deployment

Verify Purchase Orders, Deliver To selection, RFQ/PO printing, receipt creation, and dropship behavior.
