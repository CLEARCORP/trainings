# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Course (osv.Model):
    _name = 'nuevo_modulo.course'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'description': fields.text('Description'),
               }
class Student (osv.Model):
    _name = 'nuevo_modulo.student'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'birthday':fields.date('Birthday'),
        }
class CourseSession (osv.Model):
    _name = 'nuevo_modulo.session'
    _columns = {
        'subject': fields.char('Subject', size=256, required=True, select=True),
        'start_time': fields.char('Start time', required=True),
        'end_time': fields.char('End time'),
        }
 