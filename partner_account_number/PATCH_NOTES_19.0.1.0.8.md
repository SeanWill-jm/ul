# Patch Notes — 19.0.1.0.8

## Uniqueness checks run globally (`sudo()`)

The account-number suffix and the branch prefix are **global** invariants: unique across
every company and branch. Until 1.0.7 the friendly pre-save duplicate checks and the
prefix→branch lookup ran under the importing user's record rules, so a partner or
company in a company not currently enabled in the company switcher could be missed:

- the duplicate check would fall through to the raw database constraint message
  ("duplicate key value violates unique constraint ...") instead of
  "Account sequence 036798 is already used by <partner> (<account>)";
- a valid branch prefix belonging to a company not enabled in the switcher could be
  treated as unassigned, sending the number to the current company instead.

Both searches now use `sudo()` (with `active_test=False`, as before). Scope of the
elevation is minimal: read-only searches that return at most one record, from which only
`display_name` and `customer_account_no` are read for the error text. No write, create or
unlink is performed under `sudo()`, and the database constraints remain the final guard.

Reported while importing on staging (2026-09-02) alongside the standard multi-company
read error on partners whose Company is set — that error is Odoo's `res.partner company`
record rule on the *target* records of an update-import and is resolved by enabling the
relevant companies in the switcher; it is unrelated to this change.

No view, sequence, import-format or business-rule change.

## Validation status

Odoo.sh staging 2026-09-03: upgrade clean, **18/18 tests pass**. Full CSV import is the remaining UAT step.
