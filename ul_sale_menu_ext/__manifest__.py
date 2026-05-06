{
    'name': 'UL Sale Menu Extension',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Add Accounting menus in Sales',
    'description': """
        Add existing Accounting menus in Sale Order application:
        - Invoice
        - Credit Note
        - Account Receivable
    """,
    'depends': ['sale', 'account', 'account_reports'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_menus.xml',
    ],
    'installable': True,
    'application': False,
}
