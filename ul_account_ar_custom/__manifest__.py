{
    'name': 'UL AR Report Customization',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'AR Report: Sales Rep & Branch filters + Due Date column',
    'depends': ['account_reports', 'point_of_sale', 'stock', 'sale_stock'],
    'data': [
        'data/aged_receivable_due_date_column.xml',
        'views/res_config_settings_view.xml',
        'views/product_template_views.xml',
        'views/product_catalog_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ul_account_ar_custom/static/src/components/**/*',
        ],
    },
    'license': 'LGPL-3',
}
