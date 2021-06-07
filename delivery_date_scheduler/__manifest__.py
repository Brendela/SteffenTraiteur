# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    "name": "Delivery Date Scheduler",
    "author": "AppJetty",
    'license': 'OPL-1',
    "version": "14.0.1.0.2",
    "category": "Website",
    "website": "https://www.appjetty.com",
    "description": "This module is used for add customer order delivery datetime and time slot section at payment page",
    "summary": "This module is used for add customer order delivery datetime  and time slot section at payment page",
    "depends": [
            'website',
            'sale_management',
            'website_sale',
            'base_setup',

    ],
    "data": [
        'data/dayoff_setting.xml',
        'views/sale_order_view.xml',
        'views/order_delivery_pro_config_view.xml',
        'views/customer_order_delivery_config_view.xml',
        'views/my_delivery_date_view.xml',
        'views/order_pro_template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'images': ['static/description/splash-screen.png'],
    'auto_install': False,
    'price': 99.00,
    'currency': 'EUR',
    'support': 'support@appjetty.com',
}
