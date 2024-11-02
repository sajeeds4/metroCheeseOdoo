# -*- coding: utf-8 -*-
# from odoo import http


# class StockInvoiceDownload(http.Controller):
#     @http.route('/stock_invoice_download/stock_invoice_download', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_invoice_download/stock_invoice_download/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_invoice_download.listing', {
#             'root': '/stock_invoice_download/stock_invoice_download',
#             'objects': http.request.env['stock_invoice_download.stock_invoice_download'].search([]),
#         })

#     @http.route('/stock_invoice_download/stock_invoice_download/objects/<model("stock_invoice_download.stock_invoice_download"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_invoice_download.object', {
#             'object': obj
#         })
