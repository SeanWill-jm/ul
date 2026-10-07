{
    "name": "Partner Account Number",
    "summary": "Branch-prefixed, globally unique customer/vendor account numbers",
    "version": "19.0.1.0.8",
    "category": "Contacts",
    "author": "SWIT Global Consultants",
    "license": "LGPL-3",
    "depends": ["base", "contacts"],
    "data": [
        "data/ir_sequence.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "application": False,
}
