# Security Review (19.0.1.0.1)

## New security objects

None: no new model, ACL, record rule or menu. One data record: the contact tag.

## Access behaviour

Standard Purchase, Contact and multi-company rules stay authoritative. Anyone who can edit a PO
can choose a tagged contact they are allowed to read.

## Implementation safety

- One read-only `sudo()`: the constraint checks the selected contact's tags, so a narrowed
  company switcher cannot hide the tag and cause a false rejection.
- No raw SQL, no controller, no new endpoint.
- The dropdown domain is client-side only; the constraint enforces the tag on write/import.
- The field is `ondelete="restrict"`: a contact used as a Delivery Address on any PO cannot be
  deleted (archive it instead).
- Portal: the address is rendered from the order the portal controller already exposes.
- Anyone able to edit contacts can tag a contact, and thereby make it selectable on POs.
