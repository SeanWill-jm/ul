# Installation — Odoo.sh 19.0

## Prerequisites

- Odoo.sh 19.0 project.
- Purchase and Inventory applications.
- Development or Staging branch.

## Steps

1. Copy `purchase_warehouse_delivery_address` to `~/src/user/`.
2. Commit and push:

```bash
cd ~/src/user
git add purchase_warehouse_delivery_address
git commit -m "Add Purchase Warehouse Delivery Address module"
git push
```

3. Wait for a green Odoo.sh build.
4. Connect to the test database.
5. Activate Developer Mode.
6. Go to **Apps → Update Apps List → Update**.
7. Search for **Purchase Warehouse Delivery Address**.
8. Verify version `19.0.1.0.0`.
9. Install/Activate.

Install first in Development or Staging, not directly in Production.
