# Patch Notes — 19.0.1.0.5

## Prefix precedence correction for legacy imports

19.0.1.0.4 let a supplied **Account Branch** column override the current company for
prefix-less values, and rejected values whose prefix is not assigned to any branch
(for example `100-36798` when 100 is unassigned). Both contradicted the approved rule.

Rules as of 19.0.1.0.5:

1. **Assigned prefix in the value wins.** `101-36798` → `101-036798` and the Account
   Branch becomes the 101 branch, regardless of the company the import runs in.
   If an Account Branch column is also supplied it must be that same branch.
2. **Otherwise the current company wins.** No prefix (`30049`, `-36798`) or an
   unassigned prefix (`100-36798`) → prefix of the company selected while importing,
   which becomes the Account Branch. A supplied Account Branch column is ignored for
   these rows. The current company must have an Account Prefix.
3. The numeric part is zero-padded to six digits; the original value is kept in
   **Legacy Account No.** whenever it differs from the stored value.

| CSV value | Importing in company | Stored Customer Account No. | Legacy Account No. |
|---|---|---|---|
| `30049` | 101 | `101-030049` | `30049` |
| `30049` | 102 | `102-030049` | `30049` |
| `-36798` | 103 | `103-036798` | `-36798` |
| `-36798` | 101 | `101-036798` | `-36798` |
| `100-36798` (100 unassigned) | 103 | `103-036798` | `100-36798` |
| `101-36798` | 103 | `101-036798` | `101-36798` |
| `102-36798` | 102 | `102-036798` | `102-36798` |
| `103-062001` | any | `103-062001` | (empty) |

Uniqueness, immutability, archive-instead-of-delete and automatic generation
(sequence from `062001`, skipping occupied suffixes) are unchanged.

## Tests

- Test 09 rewritten: prefix-less value + Account Branch column → current company wins.
- Test 15: unassigned prefix falls back to current company, raw value kept.
- Test 16: assigned prefix in value wins over current company.
- Test 17: importing a prefix-less value while the current company has no Account Prefix
  is rejected.

## Validation status

Python syntax and XML/CSV well-formedness validated in the build environment.
Runtime installation, unit tests and CSV import remain to be validated on an Odoo.sh
development/staging branch.
