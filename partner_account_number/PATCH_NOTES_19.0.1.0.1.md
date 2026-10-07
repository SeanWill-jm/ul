# Patch Notes — 19.0.1.0.1

## Odoo 19 compatibility correction

The original 19.0.1.0.0 package inherited `base.view_partner_form` using:

`//div[hasclass('oe_title')]`

The Odoo 19.0 main `res.partner` form no longer contains that legacy `oe_title`
container. The account-identification block is now inserted after the main
header area using:

`//sheet/div[hasclass('mb8')]`

This matches the Odoo 19.0 `base.view_partner_form` structure.

No numbering logic, uniqueness rules, CSV-import behavior, branch-prefix logic,
or sequence start value was changed by this patch.

Target remains Odoo.sh / Odoo 19.0.
