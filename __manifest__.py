# -*- coding: utf-8 -*-
{
    'name': "user_partner_extended",

    'summary': """
        Extend res.users and res.partner method and fields""",

    'description': """
        - ADD res.users new field classification (customer,vendor,admin)
        - ADD res.partner several info fields
        - ADD product classification (service, cost)
        - ADD partner product.supplierinfo relation to create subscriptions to products from partner creation
        - ADD docs_check field to know when vendor needs documents check
        - ADD create partnet stripe connect account  
    """,

    'author': "pmmarquez@gmx.com",

    'category': 'Administration',
    'version': '0.1',
    
    'depends': ['base','product','payment_stripe'],

    # always loaded
    'data': [
    #     # 'security/ir.model.access.csv',
    #     'views/views.xml',
    #     'views/templates.xml',
        'actions/ir_cron_partner_check.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
