from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    dimensions = fields.Char(string="dimensions")
    sale_order_line_id = fields.Many2one('sale.order.line', string="sale order line")