# -*- coding: utf-8 -*-
# from odoo import http


# class ProductCatalogCustomization(http.Controller):
#     @http.route('/product_catalog_customization/product_catalog_customization', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_catalog_customization/product_catalog_customization/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_catalog_customization.listing', {
#             'root': '/product_catalog_customization/product_catalog_customization',
#             'objects': http.request.env['product_catalog_customization.product_catalog_customization'].search([]),
#         })

#     @http.route('/product_catalog_customization/product_catalog_customization/objects/<model("product_catalog_customization.product_catalog_customization"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_catalog_customization.object', {
#             'object': obj
#         })

