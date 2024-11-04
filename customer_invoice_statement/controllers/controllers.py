# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerInvoiceStatement(http.Controller):
#     @http.route('/customer_invoice_statement/customer_invoice_statement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_invoice_statement/customer_invoice_statement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_invoice_statement.listing', {
#             'root': '/customer_invoice_statement/customer_invoice_statement',
#             'objects': http.request.env['customer_invoice_statement.customer_invoice_statement'].search([]),
#         })

#     @http.route('/customer_invoice_statement/customer_invoice_statement/objects/<model("customer_invoice_statement.customer_invoice_statement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_invoice_statement.object', {
#             'object': obj
#         })

