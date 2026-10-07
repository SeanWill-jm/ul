# Installation Notes

The ZIP contains the installable addon folder `website_sale_catalog_tiles/`.

Target: **Odoo.sh 19.0**. Depends on `website_sale_stock` (Website, eCommerce,
Inventory).

Statically checked (Python syntax, XML well-formedness, XPath anchors compared
with the 19.0 source views, SCSS syntax) before delivery. Runtime installation
and the 4 HttpCase tests must still be run on the Odoo.sh staging branch.

```bash
# copy the folder into ~/src/user/website_sale_catalog_tiles, then
odoo-bin -d $PGDATABASE -i website_sale_catalog_tiles --stop-after-init
odoosh-restart http
# tests
odoo-bin -d $PGDATABASE -u website_sale_catalog_tiles --test-enable --test-tags /website_sale_catalog_tiles --stop-after-init
# commit so the module survives the next rebuild
cd ~/src/user && git add website_sale_catalog_tiles && git commit -m "Add website_sale_catalog_tiles 19.0.1.0.0" && git push https HEAD:test
```

Then follow `CONFIGURATION_RUNBOOK_unique_living_websites.md` (same folder as
this ZIP) for the two websites.
