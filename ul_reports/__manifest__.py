{
    'name': 'UL Reports',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Custom PDF Reports for UL: Invoice, Proforma, Purchase Order, Distributor Invoice',
    'author': 'Rmeta Technologies',
    'website': 'https://www.rmetatech.com/',
    'depends': ['ul_account_ar_custom', 'account', 'purchase', 'sale'],
    'data': [
        'views/report_fields_views.xml',
        'reports/invoice_report.xml',
        'reports/proforma_invoice_report.xml',
        'reports/purchase_order_report.xml',
        'reports/distributor_invoice_report.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
