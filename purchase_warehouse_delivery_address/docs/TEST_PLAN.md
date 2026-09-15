# Test and UAT Plan

## Automated tests

The included TransactionCase verifies:

1. Delivery Address resolves from the warehouse selected by Deliver To.
2. Changing Deliver To changes the derived Delivery Address.
3. The field is a read-only related field through the expected model chain.

## UAT-01 — Warehouse A

Select Warehouse A under Deliver To, confirm the Delivery Address, and print the RFQ. Expected: Warehouse A address prints.

## UAT-02 — Warehouse B

Change Deliver To to Warehouse B. Expected: displayed and printed address changes to Warehouse B.

## UAT-03 — Receipt alignment

Confirm the PO and open the generated Receipt. Expected: the receipt uses the same warehouse selected under Deliver To.

## UAT-04 — Dropship

Use a standard dropship purchase with Dropship Address. Expected: customer shipping address remains standard and the internal warehouse block is not duplicated.

## UAT-05 — RFQ and PO printing

Print once in RFQ stage and again after confirmation. Expected: correct Delivery Address on both documents.

All UAT cases must pass on Staging before Production.
