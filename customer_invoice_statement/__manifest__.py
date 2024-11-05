# __manifest__.py
{
    'name': 'Customer Statement Report',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Generates customer statements in PDF format',
    'description': 'Module to generate a customer statement report showing invoices and outstanding balances.',
    'author': 'Your Name',
    'depends': ['account', 'web'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        # 'report/customer_statement_report.xml',
    ],
    'installable': True,
    'application': False,
}
