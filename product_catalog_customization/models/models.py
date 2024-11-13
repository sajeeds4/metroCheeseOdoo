# # -*- coding: utf-8 -*-
#
from odoo import models, fields, api


# from odoo.addons.stock.models.product import Product

# def _compute_quantities(self):
#     products = self.with_context(prefetch_fields=False).filtered(lambda p: p.type != 'service').with_context(
#         prefetch_fields=True)
#     res = products._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'),
#                                             self._context.get('package_id'), self._context.get('from_date'),
#                                             self._context.get('to_date'))
#     res['']
#     for product in products:
#         product.update(res[product.id])
#     # Services need to be set with 0.0 for all quantities
#     services = self - products
#     services.qty_available = 0.0
#     services.incoming_qty = 0.0
#     services.outgoing_qty = 0.0
#     services.virtual_available = 0.0
#     services.free_qty = 0.0
#
# Product._compute_quantities = _compute_quantities
#
class Product(models.Model):
    _inherit = "product.product"

    available_qty = fields.Float(string="Not Reserved QTYs", compute="_not_reserved_qtys")

    def _not_reserved_qtys(self):
        for rec in self:
            rec.available_qty = rec.qty_available - rec.outgoing_qty
