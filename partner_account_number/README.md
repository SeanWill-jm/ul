# Partner Account Number — Odoo.sh 19.0

Installable Odoo 19.0 custom module for branch-prefixed Customer/Vendor account numbering.

## Approved numbering rule

Format: `PPP-NNNNNN`

- `PPP` = unique three-digit Odoo company/branch prefix.
- `NNNNNN` = globally unique six-digit sequence.
- First automatically issued new suffix = `062001`.

Examples:

- `103-062001`
- `103-062002`
- `103-062003`
- `101-062004`

The six-digit portion can never be reused under another prefix.

## Fields added to Contacts (`res.partner`)

- **Customer Type**: Customer / Vendor / Customer & Vendor
- **Customer Account No.**
- **Account Branch**
- **Legacy Account No.** (read-only; original legacy value when normalization was applied)
- hidden technical **Account Sequence**

## Field added to Company/Branch (`res.company`)

- **Account Prefix** — exactly three digits, globally unique.

## Core controls

- One global `ir.sequence`, padded to six digits.
- Sequence starts at numeric value `62001`, displayed as `062001`.
- Automatic generation when Customer Type is selected and no account number is supplied.
- Manual/CSV migration numbers are accepted if valid and unique.
- Legacy numbers (`30007`, `-36798`, `103-1234`, `100-36798`) are normalized to
  `PPP-NNNNNN`: an assigned prefix in the value is kept, otherwise the current company's
  prefix is used; the original value is kept in Legacy Account No.
- Account Branch is inferred from a supplied prefix when possible.
- If an imported/manual value already occupies a future sequence number, the generator skips it.
- Full account number has a database unique constraint.
- Six-digit suffix has a separate database unique constraint.
- Branch prefix has a database unique constraint.
- Issued account numbers cannot be changed, cleared, or recycled.
- Account Branch cannot be changed after number issuance.
- Numbered contacts cannot be deleted; archive them instead.
- Archived contacts are included in duplicate checks.

## Important Odoo behavior

`Customer Type` is a custom migration/business classification. It does **not** replace Odoo's native customer/vendor commercial logic or accounting ranks.

## Install on Odoo.sh

1. Create a development branch from production.
2. Copy the `partner_account_number` folder into the Git repository.
3. Commit and push.
4. Let Odoo.sh rebuild the branch.
5. Open the development database.
6. Apps → Update Apps List if required.
7. Search for **Partner Account Number** and install it.
8. Configure **Account Prefix** on each relevant company/branch.
9. Test manual creation and CSV migration in development/staging.
10. Promote only after successful UAT.

## Branch setup

Go to **Settings → Users & Companies → Companies** and configure the three-digit **Account Prefix** on every branch used for account numbering.

Example:

| Branch | Account Prefix |
|---|---|
| Branch A | 103 |
| Branch B | 101 |
| Branch C | 102 |
| Branch D | 104 |

A prefix can belong to only one branch/company.

## CSV migration

The module fields are normal stored `res.partner` fields and are available to Odoo import.

Recommended columns:

```csv
External ID,Name,Customer Type,Account Branch/External ID,Customer Account No.
managemore_001,ABC Hardware,Customer,,103-061900
managemore_002,XYZ Supplies,Vendor,,103-061901
managemore_003,New Customer,Customer,branch_external_id,
```

### Existing ManageMore numbers

When `Customer Account No.` is populated:

- Canonical `PPP-NNNNNN` values are stored as-is.
- Legacy values are normalized (since 19.0.1.0.4, precedence fixed in 19.0.1.0.5):
  - A prefix that belongs to an assigned branch is kept: `101-36798` → `101-036798`,
    whatever company the import runs in.
  - No prefix, or a prefix no branch owns, takes the **current company** selected in Odoo
    while importing: `30007` → `103-030007`, `-36798` → `103-036798`,
    `100-36798` → `103-036798` (when importing in the 103 branch and 100 is unassigned).
    The Account Branch column is ignored for these rows.
  - Values where the export dropped the dash are split as three-digit prefix + suffix:
    `10240048` → `102-040048`, `101000001` → `101-000001` (same prefix rules apply).
  - The numeric part is zero-padded: `103-1234` → `103-001234`.
  - The original value is stored in **Legacy Account No.**
- The six-digit suffix is checked globally across all prefixes.
- If Account Branch is blank and the value carries a prefix, Odoo finds the branch from `PPP`.
- If Account Branch is supplied, its prefix must match `PPP`.

Before importing prefix-less (or unassigned-prefix) legacy rows, switch to the
branch/company they belong to (company switcher, top right). Import each branch's file
while that branch is the current company.

### Generate new numbers during import

When `Customer Type` is populated and `Customer Account No.` is blank, Odoo generates the next available suffix beginning with `062001`.

For deterministic migration, explicitly import **Account Branch/External ID** for new rows that need auto-generated numbers. If no branch is supplied, the current Odoo company/branch must have an Account Prefix configured.

## Sequence maintenance

- Code: `partner.account.number`
- Padding: `6`
- Initial next numeric value: `62001`
- Implementation: `standard`
- Company: global
- Sequence XML uses `noupdate="1"`, so ordinary module upgrades do not reset it.

Before production go-live, audit the migrated ManageMore account list. If any imported suffix at or above `062001` exists, the generator automatically skips it when reached. If many higher numbers already exist, setting the sequence to the highest migrated suffix + 1 can avoid unnecessary skipping.

## Tests included

The module contains Odoo tests covering branch inference, sequence skipping, global suffix uniqueness, prefix/branch mismatch rejection, immutability, and delete prevention.

## Target

**Odoo.sh / Odoo 19.0**

Odoo Online does not support arbitrary custom Python modules.
