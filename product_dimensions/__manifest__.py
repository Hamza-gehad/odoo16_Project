{
    'name': 'product dimension',
    'author': 'hamza',
    'depends': ['sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/product_template.xml',
        'views/sale_order_line.xml',
        'views/stock_move.xml',
        'views/account_move.xml',

    ]
}
