# Patch Notes — 19.0.1.0.6

## Test-suite hardening for real databases

19.0.1.0.5 upgraded cleanly on Odoo.sh staging (new column, sequence and all inherited
views loaded), but its test suite failed in `setUpClass`:

`duplicate key value violates unique constraint "res_company_partner_account_prefix_unique"
DETAIL: Key (partner_account_prefix)=(103) already exists.`

The tests created fixture branches with hardcoded prefixes (100, 103) and used fixed
suffixes (062001, 30007, …). That works on an empty database but collides with the real
103 branch and with migrated numbers on staging/production databases.

Tests now choose everything at runtime from values that are free in the database:
branch prefixes from the 9xx range, supplied suffixes from the top of the 0xxxxx range
(so the legacy five-digit form round-trips through zero-padding), and a generator start
in the 7xxxxx range (the sequence change is rolled back with the test
transaction, like all fixtures). Test coverage is unchanged (01–17).

A second staging run (16/17 passing) showed test 14 depending on the sequence position
left by test 02 — PostgreSQL sequences advance outside transaction rollback. The counter
is now reset in `setUp` before every test.

No model, view, sequence, import or business-logic change. Safe to deploy as an
upgrade; production behaviour is identical to 19.0.1.0.5.

## Validation status

- 19.0.1.0.5 → runtime upgrade on Odoo.sh staging: **PASS** (2026-09-02).
- 19.0.1.0.6 on Odoo.sh staging (2026-09-02): upgrade clean, **17/17 tests pass**
  against the real database. Legacy CSV import per branch is the remaining UAT step.
