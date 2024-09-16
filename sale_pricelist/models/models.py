# custom_pricelist/models/sale_order.py
from odoo import api, fields, models, _


class SaleOrderPricelist(models.Model):
    _inherit = 'sale.order'

    secondary_pricelist_id = fields.Many2one(
        'product.pricelist', string='Secondary Pricelist',
        help='Select a secondary pricelist for price comparison.'
    )

    def action_update_prices(self):
        self.ensure_one()

        self._recompute_prices()

        if self.pricelist_id:
            self.message_post(body=_(
                "Product prices have been recomputed according to pricelist %s.",
                self.pricelist_id._get_html_link(),
            ))
        if self.secondary_pricelist_id:
            self.action_compute_prices()

    def action_compute_prices(self):
        self.ensure_one()
        self._recompute_secondary_prices()


    def _recompute_secondary_prices(self):
        lines_to_recompute = self.order_line.filtered(lambda line: not line.display_type)
        lines_to_recompute.invalidate_recordset(['secondary_pricelist_item_id'])
        lines_to_recompute._compute_price_unit()
        # Special case: we want to overwrite the existing discount on _recompute_prices call
        # i.e. to make sure the discount is correctly reset
        # if pricelist discount_policy is different than when the price was first computed.
        lines_to_recompute.discount = 0.0
        lines_to_recompute._compute_discount()
        self.show_update_pricelist = False


class SaleOrderLinePricelist(models.Model):
    _inherit = 'sale.order.line'

    secondary_pricelist_id = fields.Many2one(
        'product.pricelist', related='order_id.secondary_pricelist_id'
    )

    secondary_pricelist_item_id = fields.Many2one(
        comodel_name='product.pricelist.item',
        compute='_compute_secondary_pricelist_item_id')


    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.secondary_pricelist_id', 'secondary_pricelist_id')
    def _compute_secondary_pricelist_item_id(self):
        for line in self:
            if not line.product_id or line.display_type or not line.order_id.secondary_pricelist_id:
                line.secondary_pricelist_item_id = False
            else:
                line.secondary_pricelist_item_id = line.order_id.secondary_pricelist_id._get_product_rule(
                    line.product_id,
                    line.product_uom_qty or 1.0,
                    uom=line.product_uom,
                    date=line.order_id.date_order,
                )

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0:
                continue
            if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
                line.price_unit = 0.0
            if line.order_id.secondary_pricelist_id:
                if not line.secondary_pricelist_item_id:
                    pass
                price = line.with_company(line.company_id)._get_secondary_display_price()
                line.price_unit = min(line.price_unit, price)
            else:
                price = line.with_company(line.company_id)._get_display_price()
                line.price_unit = line.product_id._get_tax_included_unit_price(
                    line.company_id,
                    line.order_id.currency_id,
                    line.order_id.date_order,
                    'sale',
                    fiscal_position=line.order_id.fiscal_position_id,
                    product_price_unit=price,
                    product_currency=line.currency_id
                )


    def _get_secondary_display_price(self):
        """Compute the displayed unit price for a given line.

        Overridden in custom flows:
        * where the price is not specified by the pricelist
        * where the discount is not specified by the pricelist

        Note: self.ensure_one()
        """
        self.ensure_one()

        pricelist_price = self._get_secondary_pricelist_price()

        if self.order_id.secondary_pricelist_id.discount_policy == 'with_discount':
            return pricelist_price

        if not self.secondary_pricelist_item_id:
            # No pricelist rule found => no discount from pricelist
            return pricelist_price

        # base_price = self._get_sec_pricelist_price_before_discount()

        # negative discounts (= surcharge) are included in the display price
        return pricelist_price

    def _get_secondary_pricelist_price(self):
        """Compute the price given by the pricelist for the given line information.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        self.ensure_one()
        self.product_id.ensure_one()

        pricelist_rule = self.secondary_pricelist_item_id
        order_date = self.order_id.date_order or fields.Date.today()
        product = self.product_id.with_context(**self._get_sec_product_price_context())
        qty = self.product_uom_qty or 1.0
        uom = self.product_uom or self.product_id.uom_id

        price = pricelist_rule._compute_price(
            product, qty, uom, order_date, currency=self.currency_id)
        print("price computed from sec price rule is", price)

        return price

    def _get_sec_product_price_context(self):
        """Gives the context for product price computation.

        :return: additional context to consider extra prices from attributes in the base product price.
        :rtype: dict
        """
        self.ensure_one()
        res = {}

        # It is possible that a no_variant attribute is still in a variant if
        # the type of the attribute has been changed after creation.
        no_variant_attributes_price_extra = [
            ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
                lambda ptav:
                    ptav.price_extra and
                    ptav not in self.product_id.product_template_attribute_value_ids
            )
        ]
        if no_variant_attributes_price_extra:
            res['no_variant_attributes_price_extra'] = tuple(no_variant_attributes_price_extra)

        return res

    # def _get_sec_pricelist_price_before_discount(self):
    #     """Compute the price used as base for the pricelist price computation.
    #
    #     :return: the product sales price in the order currency (without taxes)
    #     :rtype: float
    #     """
    #     self.ensure_one()
    #     self.product_id.ensure_one()
    #
    #     pricelist_rule = self.secondary_pricelist_item_id
    #     order_date = self.order_id.date_order or fields.Date.today()
    #     product = self.product_id.with_context(**self._get_sec_product_price_context())
    #     qty = self.product_uom_qty or 1.0
    #     uom = self.product_uom
    #
    #     if pricelist_rule:
    #         pricelist_item = pricelist_rule
    #         if pricelist_item.pricelist_id.discount_policy == 'without_discount':
    #             # Find the lowest pricelist rule whose pricelist is configured
    #             # to show the discount to the customer.
    #             while pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id.discount_policy == 'without_discount':
    #                 rule_id = pricelist_item.base_pricelist_id._get_product_rule(
    #                     product, qty, uom=uom, date=order_date)
    #                 pricelist_item = self.env['product.pricelist.item'].browse(rule_id)
    #
    #         pricelist_rule = pricelist_item
    #
    #     price = pricelist_rule._compute_base_price(
    #         product,
    #         qty,
    #         uom,
    #         order_date,
    #         target_currency=self.currency_id,
    #     )
    #
    #     print("price from base discount like func is ", price)
    #
    #     return price