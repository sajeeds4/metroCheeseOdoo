# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryRestrictStock(http.Controller):
#     @http.route('/inventory_restrict_stock/inventory_restrict_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_restrict_stock/inventory_restrict_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_restrict_stock.listing', {
#             'root': '/inventory_restrict_stock/inventory_restrict_stock',
#             'objects': http.request.env['inventory_restrict_stock.inventory_restrict_stock'].search([]),
#         })

#     @http.route('/inventory_restrict_stock/inventory_restrict_stock/objects/<model("inventory_restrict_stock.inventory_restrict_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_restrict_stock.object', {
#             'object': obj
#         })

