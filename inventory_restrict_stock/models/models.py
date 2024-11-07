# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderAvlQty(models.Model):
    _inherit = 'sale.order.line'

    available_qty = fields.Integer(string='Available Quantity', compute='_compute_avl_qty')

    @api.depends('product_id', 'product_id.qty_available', 'product_id.virtual_available', 'product_uom_qty')
    def _compute_avl_qty(self):
        for line in self:
            quantity_on_hand = 0
            reserved_quantity = 0
            # line.available_qty = line.product_id.qty_available - line.product_id.virtual_available
            line.available_qty = 0

            if line.product_id:
                warehouse = self.env['stock.warehouse'].search([('id', '=', 1)])
                quants = self.env['stock.quant'].search(
                    [('product_id', '=', line.product_id.id), ('location_id', '=', warehouse.lot_stock_id.id),
                     ('quantity', '>', 0)])
                for obj in quants:
                    if obj.product_id == line.product_id:
                        quantity_on_hand += obj.quantity
                        reserved_quantity += obj.reserved_quantity

                # print("available for CSB120", (quantity_on_hand - reserved_quantity))
                line.available_qty = quantity_on_hand - reserved_quantity


class SaleOrderAvlValidation(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for line in self.order_line:
            if line.product_uom_qty > line.available_qty:
                raise models.ValidationError(
                    'The Ordered Quantity for the Product %s is higher than what is Available in the Stock,You cannot Perform this Operation!!' % (
                        line.product_id.name))
        return res
