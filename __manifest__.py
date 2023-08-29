{
    'name': 'purchase requests',
    'author': 'hamza',
    'depends': ['purchase', 'product'],
    'data': [
        'security/security.xml',
        'data/email_data.xml',
        'security/ir.model.access.csv',
        'views/purchase_requests.xml',
        'views/purchase_order_lines.xml',
        'wizards/rej_request.xml',
        'wizards/purchase_order.xml',
        'reports/report.xml',
        'reports/request_report_template.xml'

    ]
}
