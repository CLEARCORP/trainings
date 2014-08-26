# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

#las clases en python tienen que empezar con mayuscula en cada palabra
class Course (osv.Model):
    _name = 'lesmed.course'
    
    #columnas de la tabla que se va a crear
    _columns = {
        #Nombre de la columna
        'name': fields.char ('Name', size = 128, required = True, select = True),
        'code': fields.char ('Code', size = 32, required =  True),
        'description' : fields.text('Description')
               }

class Student (osv.Model):
    _name = 'lesmed.student'
    
    _columns = {
        'name' : fields.char ('Name', size = 128, required = True, select= True),
        'code' : fields.char ('Code', size = 32, required = True, select = True ),
        'birthday' : fields.date ('Birthday')
                }
    
class CourseSession (osv.Model):
    _name = 'lesmed.course.session'
    _columns = {
        'subject' : fields.char('Subject', size=256, required = True , select = True),
        'start_time': fields.datetime('Start time', requiered = True),
        'end_time' : fields.datetime ('End time') 
                }