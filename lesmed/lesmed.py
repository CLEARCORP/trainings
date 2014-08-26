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

