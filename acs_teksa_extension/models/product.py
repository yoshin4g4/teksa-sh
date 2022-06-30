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

    @api.depends('acs_supplierinfo_id','acs_supplierinfo_id.price')
    def _get_supplier_price(self):
        for rec in self:
            acs_supplier_price = 0
            if rec.acs_supplierinfo_id:
                acs_supplier_price = rec.acs_supplierinfo_id.price
            rec.acs_supplier_price = acs_supplier_price

    acs_import_factor = fields.Float(string="IP")
    acs_supplier_price = fields.Float(string='Supplier Price', compute="_get_supplier_price", inverse='_inverse_supplier_price', compute_sudo=True)
    acs_updated_supplier_price = fields.Float(string='Updated Supplier Price')

    acs_cb_usd = fields.Float(compute="acs_compute_data", string="CB USD", store=True, compute_sudo=True)
    acs_tc = fields.Float(string="T/C")
    acs_cb_clp = fields.Float(compute="acs_compute_data", string="CB CLP", store=True, compute_sudo=True)
    acs_mul = fields.Float(string="Mul.")
    acs_list_price = fields.Float(compute="acs_compute_data", string="Priceo de Venta", store=True, compute_sudo=True)
    acs_discount = fields.Float(string="Discount")
    acs_sale = fields.Float(compute="acs_compute_data", string="Sale", store=True, compute_sudo=True)
    acs_margin = fields.Float(compute="acs_compute_data", string="Margen", store=True, compute_sudo=True)
    acs_supplierinfo_id = fields.Many2one('product.supplierinfo', compute="acs_supplier_data", string="Vendor Pricelist", compute_sudo=True)
    acs_partner_id = fields.Many2one('res.partner', related="acs_supplierinfo_id.name", string="Vendor")
    acs_supplier_product_name = fields.Char(related="acs_supplierinfo_id.product_name", string="Supplier Product Name")
    acs_supplier_product_code = fields.Char(related="acs_supplierinfo_id.product_code", string="Supplier Product Code")

    @api.onchange('acs_supplier_price')
    def _inverse_supplier_price(self):
        for rec in self:
            if rec.acs_supplierinfo_id:
                rec.acs_supplierinfo_id.price = rec.acs_supplier_price

    def acs_update_price(self):
        for rec in self:
            if rec.acs_list_price:
                rec.list_price = rec.acs_list_price
