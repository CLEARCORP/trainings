# -*- coding: utf-8 -*-
{
    'name' : 'eLearning Jornamon',
    'version' : '1.0',
    'author' : 'Jorge Nadal',
    'category' : 'Education',
    'description' : """
eLearning Jornamon
==================

This app is only for testing purposes. Most liely it will never do something usefull.
    * Red
    * Green
    * Yellow
    
    """,
    'website' : 'http://google.com',
    'images' : [],
    'depends' : [],
    'data' : [
        'jornamon_view.xml',
        'wizard/add_student_to_session.xml',
        'jornamon_menu.xml',  
        'jornamon_workflow.xml',
        'security/jornamon_security.xml',
        'security/ir.model.access.csv',     
        ],
    'qweb' : [],
    'demo' : [
        'demo/jornamon_demo.xml',
        'demo/jornamon.course.csv', 
        ],
    'test' : [],
    'installable' : True,
    'auto_install' : False,  

}