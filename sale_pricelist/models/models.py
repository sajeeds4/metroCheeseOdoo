# custom_pricelist/models/sale_order.py
from odoo import api, fields, models


class SaleOrderLinePricelist(models.Model):
    _inherit = 'sale.order.line'

    secondary_pricelist_id = fields.Many2one(
        'product.pricelist', string='Secondary Pricelist',
        help='Select a secondary pricelist for price comparison.'
    )

    @api.onchange('product_id', 'product_uom_qty', 'secondary_pricelist_id')
    def _onchange_product_id(self):
        for line in self:
            if not line.product_id or line.display_type:
                line.discount = 0.0

            if not (
                    line.order_id.pricelist_id
                    and line.order_id.pricelist_id.discount_policy == 'without_discount'
            ):
                continue

            # price_rule = line.pricelist_item_id

            if not line.pricelist_item_id:
                continue

            line = line.with_company(line.company_id)

            # Fetch the primary pricelist price
            primary_price = line._get_pricelist_price_before_discount()

            print("primary price is", primary_price)

            # Fetch the secondary pricelist price if provided
            secondary_price = None
            if line.secondary_pricelist_id:
                line.pricelist_item_id = line.secondary_pricelist_id._get_product_rule(
                    line.product_id,
                    line.product_uom_qty or 1.0,
                    uom=line.product_uom,
                    date=line.order_id.date_order,
                )
                secondary_price = line._get_pricelist_price_before_discount()
            print("secondary price is", secondary_price)

            # Get the sale price from the product master
            sale_price = line.product_id.list_price  # Use `list_price` or your desired field

            # Start with the primary price
            line.price_unit = primary_price

            # Apply the price logic
            if primary_price > sale_price:
                line.price_unit = sale_price
            else:
                line.price_unit = primary_price

            # Compare with secondary price if it exists
            if secondary_price is not None:
                if secondary_price < line.price_unit:
                    line.price_unit = secondary_price

            if not line.secondary_pricelist_id:
                line.price_unit = primary_price


