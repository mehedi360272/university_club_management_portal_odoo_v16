# -*- coding: utf-8 -*-
{
    'name': "Uniclub Core",

    'summary': """
        Core Functionality For Uni-club""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Khondokar Md. Mehedi Hasan",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/uniclub_core_club_view.xml',
        'views/uniclub_core_club_type_view.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [


    ],
}
