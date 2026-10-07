# Patch notes — 19.0.1.0.2 (2026-10-07)

Tests only; no functional change.

- Test helper `_move()` passed `name` to `stock.move.create()`; `stock.move` has no `name`
  field in 19.0 (`ValueError: Invalid field 'name' in 'stock.move'`), which errored tests
  08–12 and 14 on staging. Replaced by `description_picking`.
- Runtime result for 1.0.1 on staging 2026-10-07: upgrade clean (views + default filters
  loaded), 10/16 tests passed, 6 errors all from this fixture line.
