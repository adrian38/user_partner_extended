# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Users(models.Model):
    _inherit = 'res.users'

    classification = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Administrator')
        ], readonly=True)