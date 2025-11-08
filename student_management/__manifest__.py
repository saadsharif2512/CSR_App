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
        'views/student_views.xml',
        'views/course_views.xml',
        'views/enrollment_views.xml',
        'views/menu.xml',
        'data/demo_data.xml',
    ],
    'application': True,
}
