# Configuration Guide (19.0.1.0.1)

## Tag the delivery contacts

1. **Contacts** -> open the contact that represents a delivery site (create it if needed, with
   the full address and phone).
2. In **Tags** add **PO Delivery Address**. (Or import: column `Tags` = `PO Delivery Address`.)
3. Only tagged, active contacts appear in the PO **Delivery Address** dropdown.

Contact visibility follows the standard multi-company rules (a contact bound to another company
is not selectable unless that company is enabled in the switcher). Leave Company blank on
contacts meant to be used by every branch.

## Use on a PO / RFQ

Select **Delivery Address** under Currency. It is independent of **Deliver To**.

## Behaviour summary

- One contact at a time; can be changed or cleared in any state.
- Empty -> RFQ/PO print as standard.
- Set -> extra Delivery Address block on the PDF and the vendor portal page.
- The tag can be recoloured; do not delete it. It is noupdate data and is not reset on upgrade.

## Dropship

Standard Dropship Address keeps printing as "Shipping address". Both blocks can appear.
