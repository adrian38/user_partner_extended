# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Response
from odoo import api, fields, models, _
import werkzeug.wsgi

class Message(models.Model):
    _inherit = 'mail.message'


    message_type = fields.Selection([
        ('email', 'Email'),
        ('comment', 'Comment'),
        ('notification', 'System notification'),
        ('user_notification', 'User Specific Notification'),
        ('ranking', 'Client Vendor Ranking')],
        'Type', required=True, default='email',
        help="Message type: email for email message, notification for system "
             "message, comment for other messages such as user replies",
        )

    ranking = fields.Integer(string="provider gived ranking")