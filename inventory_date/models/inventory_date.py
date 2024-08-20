# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'product.template'
    brand=fields.Char("Brand")
    sales_unit=fields.Char("Sales Unit")
    tag=fields.Char("Tag")
    upc=fields.Char("UPC")


