# Acceptance Criteria (19.0.1.0.1)

- [ ] Upgrade from 1.0.0 completes on Staging without error (views, report, field, tag).
- [ ] Tag **PO Delivery Address** exists; only tagged contacts are selectable.
- [ ] Exactly one contact can be selected; it can be changed or cleared in any state.
- [ ] Delivery Address sits in the left column under Currency and does not conflict with Deliver To.
- [ ] RFQ PDF (both print actions) and PO PDF print the block; empty = standard output.
- [ ] Standard Dropship "Shipping address" is unchanged and can print alongside.
- [ ] Vendor portal page shows the Delivery Address.
- [ ] Optional list column, search field and Group By work on RFQ and PO lists.
- [ ] Deliver To and receipt creation behave exactly as before.
- [ ] Automated tests pass on Staging.
- [ ] Staging UAT approved before Production.
- [ ] (1.0.4) Standard Shipping address is hidden only when a Delivery Address is set.
- [ ] (1.0.4) Vendor tax number prints as `TAX ID:` exactly once on RFQ and PO; other reports unchanged.
- [ ] (1.0.4) RFQ keeps its Requested Ship Date.
