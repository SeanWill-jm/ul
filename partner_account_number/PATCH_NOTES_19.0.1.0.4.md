# Patch Notes — 19.0.1.0.4

## Legacy (ManageMore) account-number import

Importing legacy account numbers such as `30007` or `-36798` failed on 19.0.1.0.3 with:

`Customer Account No. '-36798' is invalid. Expected format: 103-062001.`

Version 19.0.1.0.4 accepts legacy forms on CSV import, RPC create/write and manual
entry, and normalizes them to the approved `PPP-NNNNNN` format:

| Supplied value | Account Branch column | Current company prefix | Stored `Customer Account No.` | Stored `Legacy Account No.` |
|---|---|---|---|---|
| `30007` | blank | 103 | `103-030007` | `30007` |
| `-36798` | blank | 103 | `103-036798` | `-36798` |
| `30049` | branch with prefix 103 | 101 | `103-030049` | `30049` |
| `103-1234` | blank | any | `103-001234` | `103-1234` |
| `103-062001` | blank | any | `103-062001` | (empty) |

Rules:

- A missing prefix is taken from the row's **Account Branch** when supplied, otherwise
  from the **current company** the import is running in. That company must have an
  Account Prefix configured.
- The numeric part is zero-padded to six digits, so legacy numbers occupy the
  `000000`–`061999` range and stay visually close to the original.
- A leading dash (an empty-prefix separator in the legacy export) is discarded.
- The original value is preserved verbatim in the new read-only field
  **Legacy Account No.** (`res.partner.legacy_account_no`) whenever normalization
  changed it. A `Legacy Account No.` column may also be supplied explicitly on import.
- All existing controls are unchanged and apply to the normalized value: global six-digit
  suffix uniqueness, full-number uniqueness, prefix/branch match, immutability after
  issuance, archive-instead-of-delete.

## Automatic generation

Unchanged. Manual creation with a Customer Type and no number still takes the branch
prefix (selected Account Branch, else current company) and the next value from the
global sequence starting at `062001`, skipping any suffix already occupied.

## UI

- Contact form: **Legacy Account No.** shown read-only when populated.
- Contact list: optional hidden column **Legacy Account No.**
- Contact search: searchable field and a **Migrated (Legacy Account No.)** filter.

## Tests

Tests 07–14 added covering prefix inference from current company and from the branch
column, leading-dash handling, short-suffix padding, canonical values leaving the legacy
field empty, global uniqueness across normalized values, rejection of invalid values, and
the generator being unaffected by the legacy range.

## Validation status

Python syntax and XML/CSV well-formedness validated in the build environment.
Runtime installation, unit tests and CSV import must be validated on an Odoo.sh
development/staging branch (the build environment has no running Odoo 19 database).
