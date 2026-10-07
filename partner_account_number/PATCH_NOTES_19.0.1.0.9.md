# Patch notes — 19.0.1.0.9 (2026-10-07)

Version: 19.0.1.0.9 · Last Updated: 2026-10-07 · Copyright © 2026 SWIT Global Consultants · Created by: SWIT Global Consultants

Documentation release; no functional change.

- Added `static/description/index.html`: the page Odoo shows under Apps › module card ›
  **Module Info** (purpose, fields with technical names, setup, user guide by role, imports,
  limits, tests, version history, standard footer).
- Removed the `website` key from `__manifest__.py`. With it present, the module card shows
  **Learn More** and redirects to an external site; without it Odoo shows **Module Info** and
  renders the page above (verified in 19.0 `base/views/ir_module_views.xml`).
- README.md carries the SWIT standard header and footer (see
  `MODULE_DOCUMENTATION_STANDARD.md` at the project folder root). The company URL now appears
  only in footer copyright lines.

Upgrade: `odoo-bin -d $PGDATABASE -u partner_account_number --stop-after-init` then `odoosh-restart http`,
or Apps › Update Apps List. No schema change.

---
License: LGPL-3 · Summary: in-app documentation page and manifest clean-up · Platform Version: Odoo 19.0 (Odoo.sh) · Status: Static checks only
Copyright © 2026 SWIT Global Consultants — https://switconsulting.com · Created by: SWIT Global Consultants
