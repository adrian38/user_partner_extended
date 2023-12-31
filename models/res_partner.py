# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Response
from odoo import api, fields, models, _
import werkzeug.wsgi
class Partner(models.Model):
    _inherit = 'res.partner'

    address_street = fields.Text('Address Street')
    address_floor = fields.Text('Address Floor')
    address_portal = fields.Text('Address Portal')
    address_number = fields.Text('Address Number')
    address_door = fields.Text('Address door')
    address_stairs = fields.Text('Address Stairs')
    address_zip_code = fields.Text('Address ZIP Code')
    address_latitude = fields.Text('Address Geo Latitude')
    address_longitude = fields.Text('Address Geo Longitude')
    vat_cif = fields.Char('CIF number')
    social_security = fields.Char('Social security number')
    iae_code = fields.Char('I.A.E code')
    dni = fields.Char('DNI number')
    document = fields.Image("Image", max_width=1920, max_height=1920)
    
    product_supply_ids = fields.One2many('product.supplierinfo', 'name')
    initial= fields.Boolean(default=False) #waiting for authrization
    docs_check = fields.Boolean(default=True) #true when partner needs docs check

    stripe_connect_account_id = fields.Char('Stripe connect account')
    stripe_connect_account_link = fields.Char('Stripe connect account link')
    stripe_connect_account_state = fields.Selection(selection=[
            ('false', 'False'),
            ('created', 'Created'),
            ('verified', 'Verified')
        ], string='Stripe connect account state', default='false')

    #Clasification fields
    clasification_sum =  fields.Integer(string="Sum of all previous clasifications", default = 0)
    count = fields.Integer(string="Count of all previous clasification", default = 0)
    ranking = fields.Float(string="provider ranking", default = 0)

    def calculate_ranking(self, ranking):
        self.count += 1
        self.clasification_sum += ranking
        self.ranking = self.clasification_sum / self.count

    def set_docs_check(self):
        users = self.env['res.users'].search([('classification', '=', 'vendor')])
        for user in users:
            user.partner_id.docs_check = True
        return True

    def stripe_express_connect_account(self, reauth_url, return_url):
        payment_stripe = self.env['payment.acquirer'].search([('provider', '=', 'stripe')])
        # create express account
        s2s_data_account = {
            'type': 'express',
            'country': 'ES',
            'email': self.email,
        }
        account = payment_stripe._stripe_request('accounts', s2s_data_account)
        # create account link
        link = self.generate_stripe_connect_account_link(account.get('id'), reauth_url, return_url)
        return_data = {
            'partner_id': self.id,
            'account_id': account.get('id'),
            'link': link.get('url'),
        }
        # return link 
        if account.get('id') and link:
            self.stripe_connect_account_id = account.get('id')
            self.stripe_connect_account_state = 'created'
            self.env['bus.bus'].sendone(
                self._cr.dbname + '_' + str(self.id),
                {'type': 'stripe_account_vendor_notification', 'action':'created', "account_id":account.get('id')})
            return return_data
        else:
            return False
    
    def generate_stripe_connect_account_link(self, account_id, reauth_url, return_url):
        payment_stripe = self.env['payment.acquirer'].search([('provider', '=', 'stripe')])
        # create account link
        s2s_data_account_link = {
            'account': account_id,
            'refresh_url': reauth_url + '?account_id=' + account_id + '&partner_id=' + str(self.id) + '&reauth_url=' + reauth_url + '&return_url=' + return_url,
            'return_url': return_url + '?account_id=' + account_id + '&partner_id=' + str(self.id) + '&reauth_url=' + reauth_url + '&return_url=' + return_url,
            'type':'account_onboarding'
        }
        link = payment_stripe._stripe_request('account_links', s2s_data_account_link)
        # return link 
        if account_id and link.get('url'):
            self.env['bus.bus'].sendone(
                self._cr.dbname + '_' + str(self.id),
                {'type': 'stripe_account_vendor_notification', 'action':'link', "link":link.get('url')})
            self.stripe_connect_account_link = link.get('url')
            return link
        else:
            return False
    
    def delete_stripe_connect_account(self):
        payment_stripe = self.env['payment.acquirer'].search([('provider', '=', 'stripe')])
        response = payment_stripe._stripe_request('accounts/%s' % self.stripe_connect_account_id, data=False, method='DELETE')
        # return link 
        if response.get('deleted'):
            self.env['bus.bus'].sendone(
                self._cr.dbname + '_' + str(self.id),
                {'type': 'stripe_account_vendor_notification', 'action':'deleted', "account_id":self.stripe_connect_account_id})
            self.stripe_connect_account_id = False
            self.stripe_connect_account_link = False
            self.stripe_connect_account_state = 'false'
            return response
        else:
            return False
    
    def verify_stripe_connect_account(self):
        payment_stripe = self.env['payment.acquirer'].search([('provider', '=', 'stripe')])
        response = payment_stripe._stripe_request('accounts/%s' % self.stripe_connect_account_id, data=False, method='GET')
        # return link 
        if response.get('payouts_enabled'):
            self.env['bus.bus'].sendone(
                self._cr.dbname + '_' + str(self.id),
                {'type': 'stripe_account_vendor_notification', 'action':'verified', "account_id":self.stripe_connect_account_id})
            self.stripe_connect_account_state = 'verified'
            return True
        else:
            return False