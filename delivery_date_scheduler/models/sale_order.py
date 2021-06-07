# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

import time
from dateutil import tz
from datetime import datetime, date
from odoo import api, fields, models
from odoo.models import Model
from lxml import etree
# from odoo.osv.orm import setup_modifiers
from odoo.addons.base.models.ir_ui_view import transfer_node_to_modifiers, transfer_modifiers_to_node


class SaleOrder(Model):

    """Adds the fields for options of the customer order delivery"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    # @api.one
    @api.depends('name', 'time_slote_id', 'time_slote_his_id')
    def get_name(self):
        res = {}
        time_slot_12_obj = self.env['delivery.timeslots']
        time_slot_24_obj = self.env['delivery.timeslots.his']
        # self.ensure_one()
        for sid in self:
            sid.slot_name = sid.name
            if sid.time_slote_id:
                slot_12 = time_slot_12_obj.browse(int(sid.time_slote_id.id))
                sid.slot_name = sid.name + " " + slot_12.name
            if sid.time_slote_his_id:
                slot_24 = time_slot_24_obj.browse(int(sid.time_slote_his_id.id))
                sid.slot_name = sid.name + " " + slot_24.name

    customer_order_delivery_date = fields.Datetime('Delivery Date Time')

    customer_order_delivery_comment = fields.Text('Delivery Comment')

    time_slote_id = fields.Many2one('delivery.timeslots', string='Delivery Time Slot')
    time_slote_his_id = fields.Many2one('delivery.timeslots.his', string='Delivery Time Slots')
    slot_name = fields.Char(string="Name", compute='get_name', store=True)
    #site_id = fields.Many2one('website', string="website")

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        website_obj = self.env['website']
        website_config_obj = self.env['res.config.settings']
        # website_config_obj = self.env['website.config.settings']
        res = super(SaleOrder, self).fields_view_get(view_id, view_type, toolbar, submenu)
        if res:
            doc = etree.XML(res['arch'])
            if view_type == 'form':
                is_customer_order_delivery_date_feature = False
                is_customer_order_delivery_comment_feature = False
                search_website_ids = website_config_obj.search(
                    [('id', '!=', False)], order='id desc', limit=1)
                for setting in search_website_ids:
                    if setting.is_customer_order_delivery_date_feature:
                        is_customer_order_delivery_date_feature = True

                    if setting.is_customer_order_delivery_comment_feature:
                        is_customer_order_delivery_comment_feature = True
                    if setting.timeformat == '24h':
                        for node in doc.xpath("//field[@name='time_slote_id']"):
                            modifiers = {}
                            node.set('invisible', '1')
                            transfer_node_to_modifiers(node, modifiers)
                            transfer_modifiers_to_node(modifiers, node)
                            # setup_modifiers(node, res['fields']['time_slote_id'])
                    else:
                        for node in doc.xpath("//field[@name='time_slote_his_id']"):
                            node.set('invisible', '1')
                            modifiers = {}
                            node.set('invisible', '1')
                            transfer_node_to_modifiers(node, modifiers)
                            transfer_modifiers_to_node(modifiers, node)
                            # setup_modifiers(node, res['fields']['time_slote_his_id'])

                if is_customer_order_delivery_date_feature:
                    for node in doc.xpath("//page[@string='Customer Order Delivery Date Time']"):
                        node.set('string', '')

                if is_customer_order_delivery_comment_feature:
                    for node in doc.xpath("//field[@name='customer_order_delivery_comment']"):
                        node.set('style', 'display:none')

                res['arch'] = etree.tostring(doc)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
