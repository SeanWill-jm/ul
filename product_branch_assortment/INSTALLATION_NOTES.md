# Installation Notes

The ZIP contains the installable addon folder `product_branch_assortment/`.

Target: **Odoo.sh 19.0**. Depends on `sale_stock` (Sales + Inventory).

The package is statically checked for Python syntax and XML well-formedness,
and its inherited-view anchors were compared with the 19.0 source views, before
delivery. It still must be installed and UAT-tested in an Odoo.sh development
or staging branch because this build environment is not a running Odoo 19
server/database.

Odoo.sh editor workflow (same as `partner_account_number`):

```bash
# copy the folder into ~/src/user/product_branch_assortment, then
odoo-bin -d $PGDATABASE -i product_branch_assortment --stop-after-init
odoosh-restart http
# tests
odoo-bin -d $PGDATABASE -u product_branch_assortment --test-enable --test-tags /product_branch_assortment --stop-after-init
# commit so the module survives the next rebuild
cd ~/src/user && git add product_branch_assortment && git commit -m "Add product_branch_assortment 19.0.1.0.0" && git push https HEAD:test
```

See `product_branch_assortment/README.md` for the business rule, configuration
and known limits, and `SPEC_product_branch_assortment.md` for the functional
specification and acceptance criteria.
