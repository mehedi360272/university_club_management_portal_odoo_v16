# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Notice Board',
    'version' : '16.0',
    'summary': 'A platform for communication and sharing important information.',
    # 'sequence': 15,
    'description': """ A notice board serves as a central location for posting announcements, news, events, and 
     other information.
     It facilitates communication and ensures that everyone stays informed and up-to-date.
     """,
    'category': 'Notice',
    'website': 'https://www.google.com',
    'images': [],
    'depends': [
        'base',
        'mail',
        'website',
    ],
    'data': [
    # Security
        'security/ir.model.access.csv',
    # Data
        'data/data.xml',
    # views
        'views/se_notice.xml',
        'views/configuration.xml',
        'views/menus.xml',
        'views/template.xml',


    ],
    'demo': [
    
    ],
    'qweb': [
    
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
