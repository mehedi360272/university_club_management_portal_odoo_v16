# -*- coding: utf-8 -*-
{
    'name': "Uniclub Application",

    'summary': """
        Application System For Member Recruitment""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Khondokar Md. Mehedi Hasan",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'uniclub_core', 'web', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'reports/report.xml',
        'reports/uniclub_member_id_card.xml',
        'template/application_session_template.xml',
        'template/application_form_template.xml',
        'views/uniclub_application_session_view.xml',
        'views/uniclub_application_view.xml',
        'views/uniclub_application_member_type_view.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
