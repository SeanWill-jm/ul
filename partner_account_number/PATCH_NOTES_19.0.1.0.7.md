# Patch Notes — 19.0.1.0.7

## Third legacy shape: prefix and number run together

The first real staging import (2026-09-02) accepted rows 0–590 (five-digit and
dash-only legacy values) and rejected rows from 591 onward, whose values look like
`10240048`, `10040049`, `101000001`: the legacy export dropped the dash, leaving the
three-digit prefix and the number concatenated.

19.0.1.0.7 accepts a bare run of 7–9 digits as `PPP` + 4–6 digit suffix and then applies
the existing precedence rules:

| CSV value | Importing in company | Stored Customer Account No. | Legacy Account No. |
|---|---|---|---|
| `10240048` | any (102 assigned) | `102-040048` | `10240048` |
| `101000001` | any (101 assigned) | `101-000001` | `101000001` |
| `10040049` | 103 (100 unassigned) | `103-040049` | `10040049` |

Runs longer than nine digits are still rejected. Everything else is unchanged.

## Tests

Test 13 now uses a 10-digit value as the "too long" case; test 18 covers the
concatenated form with an assigned and with an unassigned prefix.

## Validation status

Odoo.sh staging 2026-09-02: upgrade clean, **18/18 tests pass**. Full CSV import is the remaining UAT step.
