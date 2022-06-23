# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import math


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('acs_import_factor', 'acs_tc', 'acs_discount', 'list_price', 'acs_list_price', 'acs_mul')
    def acs_compute_data(self):
        for rec in self:
            acs_margin = 0            
            rec.acs_cb_usd = rec.list_price * rec.acs_import_factor
            rec.acs_cb_clp = math.ceil(rec.acs_cb_usd * rec.acs_tc)
            rec.acs_list_price = math.ceil(rec.acs_mul * rec.acs_cb_clp)
            rec.acs_sale = math.ceil((rec.acs_discount/100) * rec.acs_list_price)
            rec.acs_margin = ((rec.acs_sale - rec.acs_cb_clp)/(rec.acs_sale or 1)) * 100

    def acs_supplier_data(self):
        for rec in self:
            rec.acs_supplierinfo_id = rec.seller_ids and rec.seller_ids[0].id or False

    acs_import_factor = fields.Float(string="Improt Factor")
    acs_cb_usd = fields.Float(compute="acs_compute_data", string="CB USD", store=True, compute_sudo=True)
    acs_tc = fields.Float(string="T/C")
    acs_cb_clp = fields.Float(compute="acs_compute_data", string="CB CLP", store=True, compute_sudo=True)
    acs_mul = fields.Float(string="Mul.")
    acs_list_price = fields.Float(compute="acs_compute_data", string="New List Price", store=True, compute_sudo=True)
    acs_discount = fields.Float(string="Discount")
    acs_sale = fields.Float(compute="acs_compute_data", string="Sale", store=True, compute_sudo=True)
    acs_margin = fields.Float(compute="acs_compute_data", string="Margin", store=True, compute_sudo=True)
    acs_supplierinfo_id = fields.Many2one('product.supplierinfo', compute="acs_supplier_data", string="Vendor Pricelist", compute_sudo=True)
    acs_partner_id = fields.Many2one('res.partner', related="acs_supplierinfo_id.name", string="Vendor")
    acs_supplier_product_name = fields.Char(related="acs_supplierinfo_id.product_name", string="Supplier Product Name")
    acs_supplier_product_code = fields.Char(related="acs_supplierinfo_id.product_code", string="Supplier Product Code")

    
