# Patch Notes — 19.0.1.0.3

## Odoo.sh runtime view-inheritance hardening

The staging runtime rejected a search-view XPath anchored to:

`//field[@name='phone']`

Although the upstream Odoo 19 base search view currently contains that field,
the actual resolved parent view in the staging database did not expose the node
at validation time.

Version 19.0.1.0.3 removes field-specific anchors from the module's inherited
views and uses structural roots instead:

- Partner form: `//sheet`
- Partner list: `//list`
- Partner search: `//search`
- Company form: `//sheet`
- Company list: `//list`

This makes the addon materially more tolerant of Odoo.sh runtime differences
and inherited/customized parent-view structures.

No account-number generation, sequence, import, uniqueness, immutability, or
branch-prefix business logic was changed.
