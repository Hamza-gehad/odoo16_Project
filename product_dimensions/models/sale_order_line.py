from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    stock_move = fields.Many2one('stock.move', compute='find_stock')

    # @api.depends('name')
    # def find_stock(self):
    #     print(1)
    #
    #     for rec in self.env['stock.move'].search([]):
    #
    #         if rec.origin == self.name:
    #             self.stock_move=rec
    #             break
    #         else:
    #             self.stock = False



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    product_id = fields.Many2one('product.product', string="sale order line")
    dimensions = fields.Char(string="dimensions", related="product_id.dimensions")
    groups = fields.Boolean(compute='_compute_user_groups', default=False)


    @api.depends('groups')
    def _compute_user_groups(self):
        for record in self:
            user = record.env.user
            group_ids = user.groups_id.ids
            groups = record.env['res.groups'].browse(group_ids)
            group_names = groups.mapped('name')

            if "salesperson" in group_names:

                record.groups = True

            # record.groups = ', '.join(group_names)

