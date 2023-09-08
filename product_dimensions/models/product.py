from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'
    product_temp_id=fields.Many2one('product.template')