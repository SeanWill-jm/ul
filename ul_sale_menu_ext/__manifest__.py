{
    'name': 'UL Sale Menu Extension',
    'version': '1.1',
    'category': 'Sales',
    'summary': 'Add Accounting menus in Sales and Return Notifications',
    'description': """
        Add existing Accounting menus in Sale Order application:
        - Invoice
        - Credit Note
        - Account Receivable
        
        New Features:
        - Notify Salesperson on Return Picking creation.
    """,
    'depends': ['sale', 'account', 'account_reports', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_menus.xml',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
}
