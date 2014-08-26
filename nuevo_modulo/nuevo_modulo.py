# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Course (osv.Model):
    _name = 'nuevo_modulo.course'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'description': fields.text('Description'),
        'session_ids': fields.one2many('nuevo_modulo.session','course_id',string='Sessions'),
        'student_ids': fields.many2many('nuevo_modulo.student',string="Students"),
        'teacher_id': fields.many2one('res.users', string='Teachers', ondelete='set null', select=True),
               }
class Student (osv.Model):
    _name = 'nuevo_modulo.student'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'birthday':fields.date('Birthday'),
        'course_ids': fields.many2many('nuevo_modulo.course', string="Courses"),
        }
class CourseSession (osv.Model):
    _name = 'nuevo_modulo.session'
    _columns = {
        'subject': fields.char('Subject', size=256, required=True, select=True),
        'start_time': fields.datetime('Start time', required=True),
        'end_time': fields.datetime('End time'),
        'course_id': fields.many2one('nuevo_modulo.course', string='Course', required=True, select=True, ondelete='cascade'),
        }
    _rec_name ='subject'
    _order = 'start_time'
 