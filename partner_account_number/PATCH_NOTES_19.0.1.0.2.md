# Patch Notes — 19.0.1.0.2

Fixes the Odoo 19 partner list-view inheritance failure reported during installation.

The previous view targeted `//field[@name='display_name']`. The corrected view targets the root `<list>` node and appends the three custom columns inside the partner list. This avoids dependence on a particular field being present in the runtime base view.

No model, sequence, numbering, uniqueness, branch, or CSV-import logic changed.
