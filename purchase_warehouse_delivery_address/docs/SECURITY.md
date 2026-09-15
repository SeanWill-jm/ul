# Security Review

## New security objects

None. The module creates no new model, ACL, record rule, or menu.

## Access behavior

Existing Odoo Purchase, Inventory, Contact, and multi-company security remains authoritative.

## Implementation safety

- No `sudo()`.
- No raw SQL.
- No controller/API endpoint.
- No writable custom destination field.

The derived address cannot be used to bypass the standard Deliver To warehouse domain.
