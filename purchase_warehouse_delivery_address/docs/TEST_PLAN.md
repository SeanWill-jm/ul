# Test and UAT Plan (19.0.1.0.1)

## Automated tests (`tests/`, 17 cases, post_install)

01 tag exists - 02 field is single stored editable Many2one - 03 old related field gone -
04 domain lists only tagged contacts - 05 select/change/clear - 06 untagged rejected on create
and write - 07 removing tag later does not block unrelated edits - 08 editable in every state -
09 duplicate keeps address - 10 form view carries field - 11 PO report prints contact -
12 RFQ report prints contact - 13 reports unchanged when empty - 14 Deliver To untouched - 15 vendor block prints `TAX ID:` once (both templates) - 16 no tax line without VAT - 17 shipping block hidden only when a Delivery Address is set.

Tests create their own throwaway contacts; no hardcoded real data.

## UAT

- UAT-01 Tag a contact; it appears in the dropdown; an untagged contact does not.
- UAT-02 Select contact A on an RFQ; print via **Print -> Request for Quotation**; block shows.
- UAT-03 Print via the PO action after confirmation; block shows.
- UAT-04 Change to contact B on the confirmed PO; reprint shows B; chatter logs the change.
- UAT-05 Clear the field; documents print as standard.
- UAT-06 Dropship PO: "Shipping address" and "Delivery Address" both print, no overlap.
- UAT-07 Vendor portal page shows the Delivery Address.
- UAT-08 RFQ and PO lists: enable the optional column, search by address, Group By.
- UAT-09 Company switcher narrowed: selectable contacts follow standard visibility.
- UAT-10 Upgrade from 1.0.0: existing POs open, print, and show an empty Delivery Address.

- UAT-11 (1.0.4) Vendor with a TRN/VAT: RFQ and PO print `TAX ID: <number>` once; no `VAT:` anywhere.
- UAT-12 (1.0.4) PO with Dropship Address and no Delivery Address: standard Shipping address still prints.
- UAT-13 (1.0.4) Same PO after choosing a Delivery Address: Shipping address gone, Delivery Address present; RFQ still shows Requested Ship Date.
- UAT-14 (1.0.4) Vendor block still shows name, address, phone; send an RFQ email and check the attached PDF.

All UAT cases must pass on Staging before Production.
