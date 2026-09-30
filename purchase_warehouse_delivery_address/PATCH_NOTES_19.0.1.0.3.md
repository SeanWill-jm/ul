# Patch notes — 19.0.1.0.3

**Type:** test fix only. No functional change to the module.
**Runtime validation status:** 1.0.2 upgrade PASS on Staging 2026-09-30; tests 13/14 passed.
This version's test run is **not yet validated**.

## Runtime result that triggered this version (Staging, 2026-09-30, 1.0.2)

`0 failed, 1 error(s) of 14 tests`. Only `test_08_editable_in_every_state` errored:
`ValueError: Wrong value for purchase.order.state: 'done'`.
Passed: 01-07 and 09-14 (including both report renderings, RFQ and PO).

## Root cause

The test hardcoded the pre-18 state list (`draft, sent, purchase, done, cancel`). The 19.0
`state` selection has no `done`; locking is the separate boolean `locked`. The module code was not
involved.

## Change

- Test 08 reads the states from `purchase.order._fields['state'].selection` and, for each state,
  writes both `locked=False` and `locked=True` before changing the Delivery Address.
- Manifest version 19.0.1.0.3.

## What did not change

Model, views, reports, portal, tag, constraint.
