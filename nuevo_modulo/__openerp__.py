# -*- coding: utf-8 -*-
{
    'name': 'eLearning Management',
    'version': '1.0',
    'author': 'Oscar Gutierrez',
    'category': 'Education',
    'description': '''
eLearning Management
====================
This app is used to manage 
   
   -Courses
   -Students
   -Teachers
   -Classes
''',
    'images': [],
    'depends': [],
    'data': [
         'nuevo_modulo_view.xml',
         'wizard/add_student_to_session.xml',
         'security/nuevo_modulo_security.xml',
         'security/ir.model.access.csv',
         'nuevo_modulo_workflow.xml',
         'nuevo_modulo_menu.xml',
             ],
    'demo': [
         'demo/nuevo_modulo_demo.xml'
         'demo/nuevo_modulo.course.csv'
             ],
    'test': [],
    'installable': True,
    'auto_install': False,  
}