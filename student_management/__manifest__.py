# -*- coding: utf-8 -*-
{
    'name': 'EduTrack: Student Management',
    'summary': 'Simple student, courses, and enrollment management for workshops',
    'version': '19.0.0.0.2',
    'category': 'Education',
    'author': 'Workshop',
    'license': 'LGPL-3',
    'website': 'https://example.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_views.xml',
        'views/res_company_views.xml',
        'views/stock_views.xml',
        'views/menu.xml',
        'data/demo_data.xml',
    ],
    'application': True,
}
