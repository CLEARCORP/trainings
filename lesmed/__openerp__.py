# -*- coding: utf-8 -*-
{
    'name' : 'eLearning Management',
    'version' : '1.0',
    'author' : 'Lesmed Gutiérrez',
    'category' : 'Education',
    'description' : """ 
eLearning Management
=====================

    *Courses
    *Students
    *Classes
    *Teachers
    """, 
    'images' : [],
    'depends' : [],
    #se tiene que poner el view primero ya que tiene la accion que necesita el menu
    'data' : [
        'lesmed_view.xml',
        'lesmed_menu.xml',
              ],
    'demo' : [],
    'test' : [],
    'installable' : True,
    'auto_install' : False ,

}


