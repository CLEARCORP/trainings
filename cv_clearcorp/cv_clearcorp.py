# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class Course (osv.Model):
    _name = 'cv_clearcorp.course'
    
    def get_available_seats (self, cr, uid, ids, field_name, arg, context):
        return 0
    
    def get_occupied_seats (self, cr, uid, ids, field_name, arg, context):
        return 0
    
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'description': fields.text('Description'),
        'session_ids': fields.one2many('cv_clearcorp.course.session','course_id',string='Sessions'),
        'student_ids': fields.many2many('cv_clearcorp.student', string='Students'),
        'teacher_id': fields.many2one('res.users', string='Teacher', ondelete='set null', select=True),
        'total_seats': fields.integer('Total seats', required=True),
        'available_seats': fields.function(get_available_seats, type='integer', string='Available seats', readonly=True),
        'occupied_seats': fields.function(get_occupied_seats, type='integer', string='Occupied seats', readonly=True),
        }

class Student (osv.Model):
    _name = 'cv_clearcorp.student'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'birthday': fields.date('Birthday'),
        'course_ids': fields.many2many('cv_clearcorp.course', string='Courses')
        }

class CourseSession (osv.Model):
    _name = 'cv_clearcorp.course.session'
    _columns = {
        'subject': fields.char('Subject', size=256, required=True, select=True),
        'start_time': fields.datetime('Start time', required=True),
        'end_time': fields.datetime('End time'),
        'course_id': fields.many2one('cv_clearcorp.course', string='Course', required=True, select=True, ondelete='cascade'),
        }
    _rec_name = 'subject'
    _order = 'start_time'
