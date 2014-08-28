# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import osv, fields

class Course (osv.Model):
    _name = 'jornamon.course'
    
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
        'name' : fields.char('Name',size=128,required=True,select=True),
        'code' : fields.char('Code',size=32,required=True,select=True),
        'description' : fields.text('Description'),
        'session_ids' : fields.one2many('jornamon.course.session', 'course_id'),
        'student_ids' : fields.many2many('res.partner', string='Students', domain=[('student','=',1)]),
        'teacher_id' : fields.many2one('res.users', string='Teacher', ondelete='set null', select=True),
        'total_seats' : fields.integer('Total seats', required=True),
        'available_seats' : fields.function(get_seats, multi='seats', type='integer', string='Available seats', readonly=True),
        'occupied_seats' : fields.function(get_seats, multi='seats', type='integer', string='Atendees', readonly=True),
        'occupation_percentage': fields.function(get_seats, multi='seats', string='Percentage of occupied seats', digits=(3,1), readonly=True),
        }
    
    _defaults = {
        'teacher_id': (lambda self, cr, uid, ids, context={}: uid),
        'total_seats': 20,
        }
    
    _sql_constraints = [
        ('total_seats_positive', 'CHECK(total_seats >=0)', 'Total seats must be a positive number'),
        ]
    
    @api.multi
    def check_seats (self):
        for course in self:
            if len(course.student_ids) > course.total_seats:
                return False
        return True
             
    _constraints = [
        (check_seats, 'The course has more student than seats, you cannot add more students.', ['student_ids']),   
        (check_seats, 'You cannot set a number of seats smaller than the number of registered students.', ['total_seats']),      
        ]
    
class Partner (osv.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    _columns = {
        'student': fields.boolean('Student'),
        'birthday' : fields.date('Birthday'),
        'course_ids' : fields.many2many('jornamon.course', string='Courses'),
        'student_code' : fields.char('Student Code',size=32),        
        }
    
    
    def on_change_is_company (self, cr, uid, id, is_company, student, context={}):
        
        # Llamamos primero al método original que tenía este campo en onchange y que estamos sobreescribiendo.
        # Ahora en el diccionario de resultado AÑADIMOS nuestro resultado.
        print "**** Estamos en on_change_is_company"
        res= self.onchange_type (cr, uid, id, is_company, context=context)
        # res = {'value': {}, 'domain': {}, 'warning': {}}
        if is_company and student:
            res['value'].update({'student': False})
            res['warning'].update({'title': "Companies cannot be students",
                           'message': "You changed the partner type to company and it was a student. We have remove the student check"}) 
        return res
    
       
class Student (osv.Model):
    _name = "jornamon.student"
    
    _columns = {
        'name' : fields.char('Name',size=128, required=True, select=True),
        'code' : fields.char('Code',size=32,required=True,select=True),
        'birthday' : fields.date('Birthday'),
        'course_ids' : fields.many2many('jornamon.course', string='Courses')          
        }
    
class CourseSession (osv.Model):   
    _name = 'jornamon.course.session'
    
    #Versión de la función como se haría en v7
    """
    def button_approve (self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'pending'}, context=context)
        return True
    """
    
    #Versión de la función como se haría en v8
    @api.multi
    def button_approve (self):
        #self.write({'state': 'pending'})
        self.state= 'pending'
        return True
    
    @api.multi
    def button_start (self):
        self.state= 'open'
        return True
    
    @api.multi
    def button_done (self):
        self.state= 'done'
        return True
    
    @api.multi
    def button_cancel (self):
        self.state= 'canceled'
        return True
    
    @api.multi
    def button_reset (self):
        self.state= 'draft'
        return True
      
    _columns = {
        'subject' : fields.char('Subject', size=256, required=True, select=True, readonly=True, states={'draft':[('readonly',False)]}),
        'start_time' : fields.datetime('Start time', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'end_time' : fields.datetime('End time', readonly=True, states={'draft':[('readonly',False)]}),
        'course_id' : fields.many2one('jornamon.course', string='Course', required=True, select=True, ondelete='cascade'),
        'state': fields.selection([('draft','Draft'),
                                   ('pending','Pending'),
                                   ('open','Open'),
                                   ('done','Done'),
                                   ('canceled','Canceled')],
                                  string="State", select=True, required=True),
        'teacher_id': fields.related('course_id','teacher_id', type='many2one', relation='res.users', string='Teacher', readonly=True, store=True),
        'occupied_seats': fields.related('course_id', 'occupied_seats', string="Expected Students", type='integer', readonly=True)
        }
    
    _rec_name = 'subject'
    _order = 'start_time'
    _defaults = {
                 'state': 'draft',
                 }