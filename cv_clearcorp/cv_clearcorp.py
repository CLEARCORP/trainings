# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from openerp import api
from openerp.osv import osv, fields

class Course (osv.Model):
    _name = 'cv_clearcorp.course'
    
    @api.multi
    def get_seats (self, field_name, arg):
        res = {}
        for course in self:
            total_seats = course.total_seats
            students = course.student_ids
            occupied_seats = len(students)
            available_seats = total_seats - occupied_seats
            if total_seats:
                occupation_percentage = (occupied_seats / (total_seats * 1.0)) * 100.0
            else:
                occupation_percentage = 0.0
            res[course.id] = {
                'available_seats': available_seats,
                'occupied_seats': occupied_seats,
                'occupation_percentage': occupation_percentage,
            }
        return res
    
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'description': fields.text('Description'),
        'session_ids': fields.one2many('cv_clearcorp.course.session','course_id',string='Sessions'),
        'student_ids': fields.many2many('res.partner', string='Students', domain=[('student','=',1)]),
        'teacher_id': fields.many2one('res.users', string='Teacher', ondelete='set null', select=True),
        'total_seats': fields.integer('Total seats', required=True),
        'available_seats': fields.function(get_seats, multi='seats', type='integer', string='Available seats', readonly=True),
        'occupied_seats': fields.function(get_seats, multi='seats', type='integer', string='Occupied seats', readonly=True),
        'occupation_percentage': fields.function(get_seats, multi='seats', type='float', string='Percentage of occupied seats', digits=(3,1), readonly=True),
        }
    
    _defaults = {
        'teacher_id': (lambda self, cr, uid, ids, context={}: uid),
        'total_seats': 20,
        }
    
    _sql_constraints = [
        ('total_seats_positive', 'CHECK( (total_seats >= 0) AND (total_seats <= 100) )', 'The course\'s total seats must be a positive number.'),
        ]
    
    @api.multi
    def check_seats (self):
        for course in self:
            if len(course.student_ids) > course.total_seats:
                return False
        return True
    
    _constraints = [
        (check_seats, 'The course has more students than seats.', ['student_ids']),
        (check_seats, 'You cannot set a total seats limit under the number of actual students.', ['total_seats']),
        ]

class Partner (osv.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    _columns = {
        'student': fields.boolean('Student'),
        'birthday': fields.date('Birthday'),
        'course_ids': fields.many2many('cv_clearcorp.course', string='Courses'),
        'student_code': fields.char('Student code', size=32),
        }
    
    @api.multi
    def on_change_is_company (self, is_company, student):
        res = self.onchange_type(is_company)
        if is_company and student:
            res['value'].update({'student': False})
            res['warning'].update({'title': "Companies cannot be students",
                              'message': "You changed the partner type to company, and it was a student, we have blanked the student checkbox."})
        return res

class CourseSession (osv.Model):
    _name = 'cv_clearcorp.course.session'
    
    @api.multi
    def button_approve (self):
        #self.write({'state': 'pending'})
        self.state = 'pending'
        return True
    @api.multi
    def button_start (self):
        self.state = 'open'
        return True
    @api.multi
    def button_done (self):
        self.state = 'done'
        return True
    @api.multi
    def button_cancel (self):
        self.state = 'canceled'
        return True
    @api.multi
    def button_reset (self):
        self.state = 'draft'
        return True
    
    @api.multi
    def get_end_time (self, field_names, arg):
        res = {}
        for session in self:
            end_time = datetime.strptime(session.start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=session.duration)
            res[session.id] = datetime.strftime(end_time, '%Y-%m-%d %H:%M:%S')
        return res
    
    _columns = {
        'subject': fields.char('Subject', size=256, required=True, select=True, readonly=True, states={'draft': [('readonly',False)]}),
        'start_time': fields.datetime('Start time', required=True, readonly=True, states={'draft': [('readonly',False)]}),
        'end_time': fields.function(get_end_time, type='datetime', string='End time', readonly=True),
        'course_id': fields.many2one('cv_clearcorp.course', string='Course', required=True, select=True, ondelete='cascade', readonly=True, states={'draft': [('readonly',False)]}),
        'state': fields.selection([('draft','Draft'),
                                   ('pending','Pending'),
                                   ('open','Open'),
                                   ('done','Done'),
                                   ('canceled','Canceled')],
                                  string="State", select=True, required=True),
        'teacher_id': fields.related('course_id', 'teacher_id', type='many2one', relation='res.users', string='Teacher', readonly=True, store=True),
        'occupied_seats': fields.related('course_id', 'occupied_seats', type='integer', string='Expected students', readonly=True, store=True),
        'duration': fields.float('Duration', digits=(2,1), states={'draft': [('readonly',False)]}),
        'color': fields.integer('Color'),
        }
    _rec_name = 'subject'
    _order = 'start_time'
    
    _defaults = {
        'state': 'draft',
        }
