# Installation / Upgrade — Odoo.sh 19.0

## Prerequisites

- Odoo.sh 19.0 project, Purchase and Inventory.
- Development or Staging branch.

## Upgrade from 19.0.1.0.0 (Staging)

1. Copy `purchase_warehouse_delivery_address/` over the existing folder in `~/src/user/`.
2. From the Odoo.sh shell:

```bash
odoo-bin -d $PGDATABASE -u purchase_warehouse_delivery_address --stop-after-init
odoosh-restart http
```

3. Apps -> Purchase Delivery Address: version must read `19.0.1.0.5`.
4. Commit and push when validated:

```bash
cd ~/src/user
git add purchase_warehouse_delivery_address
git commit -m "purchase_warehouse_delivery_address 19.0.1.0.5: tagged-contact, TAX ID label Delivery Address"
git push https HEAD:test
```

## Fresh install

Apps -> Update Apps List -> search "Purchase Delivery Address" -> Install. Development or
Staging first, never directly in Production.
