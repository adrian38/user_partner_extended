# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID
from odoo.tests import Form
from math import radians, cos, sin, asin, sqrt


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        message = super(PurchaseOrder, self.with_context(
            mail_post_autofollow=True)).message_post(**kwargs)

        purchase_order = self.env['purchase.order'].search(
            [('id', '=', message.res_id)])

        partner = self.env['res.partner'].search(
            [('id', '=', purchase_order.partner_id.id)])

        if message.message_type == "ranking":
            message.ranking = kwargs['ranking']
            partner.sudo().calculate_ranking(kwargs['ranking'])
            self.env['bus.bus'].sendone(
                    self._cr.dbname + '_' + str(partner.id),
                    {'type': 'ranking_notification', 'ranking': kwargs['ranking'], "order_id": purchase_order.id, "origin": purchase_order.origin})
                
        return message
