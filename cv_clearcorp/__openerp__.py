# -*- coding: utf-8 -*-
{
    'name': 'eLearning Management',
    'version' : '1.0',
    'author' : 'Carlos Vásquez',
    'category' : 'Education',
    'description': """
eLearning Management
====================

    * Courses
    * Students
    * Classes
    * Teachers
    """,
    'images': [],
    'depends': [],
    'data': [
        'cv_clearcorp_view.xml',
        'wizard/add_student_to_session.xml',
        'cv_clearcorp_menu.xml',
        'cv_clearcorp_workflow.xml',
        'security/cv_clearcorp_security.xml',
        ],
    'demo': [
        'demo/cv_clearcorp_demo.xml',
        'demo/cv_clearcorp.course.csv',
        ],
    'test': [],
    'installable': True,
    'auto_install': False,
}