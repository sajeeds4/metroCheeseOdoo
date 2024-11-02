{
    'name': 'Custom Picking Invoice',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Generate invoices for picked quantities only',
    'depends': ['stock', 'account'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
}
