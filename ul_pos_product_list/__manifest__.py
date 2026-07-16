{
    'name': 'UL POS Product List View',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Changes POS product view to a list view',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'ul_pos_product_list/static/src/css/product_list.css',
            'ul_pos_product_list/static/src/xml/product_screen.xml',
            'ul_pos_product_list/static/src/xml/product_card.xml',
            'ul_pos_product_list/static/src/js/stock_sync.js',
            'ul_pos_product_list/static/src/js/product_card.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
