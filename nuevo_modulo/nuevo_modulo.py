# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Course (osv.Model):
    _name = 'nuevo_modulo.course'
    _columns = {
        'name': fields.char('Name',size=128,required=True,select=True),
        'code': fields.char('Code',size=32,required=True,select=True),
        'description': fields.text('Description')
               }