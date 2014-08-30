# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import osv, fields

from  datetime import datetime, timedelta


#las clases en python tienen que empezar con mayuscula en cada palabra
class Course (osv.Model):
    _name = 'lesmed.course'
    
    @api.multi
    def get_seats(self,field_name,arg):
        res = {} 
        
        #courses = self.browse(cr,uid, ids, context = context)
        for course in self:
            
            total_seats = course.total_seats
            
            students = course.student_ids
            
            occupied_seats = len(students)
            
            available_seats = total_seats  - occupied_seats
            occupation_percentage = 0.0
            
            if total_seats> 0:
                occupation_percentage = (occupied_seats / (total_seats*1.0))*100.0
            else:
                occupation_percentage = 0.0
            res[course.id] ={
                               'available_seats' : available_seats,
                               'occupied_seats' : occupied_seats,
                               'occupation_percentage' : occupation_percentage,
                            }
        return res
    
    def get_occupied_seats(self, cr, uid,ids,field_name,arg,context={}):
        
        res = {}
        for id in ids:
            course = self.browse(cr,uid, id, context=context)
            total_seats = course.total_seats
            students = course.student_ids
            occupied_seats = len(students)
            
            res[id] = occupied_seats
             
        return res
    
    @api.multi
    def check_seats(self):
        for course in self:
            if len(course.student_ids)> course.total_seats:
                return False
        return True
    
    #columnas de la tabla que se va a crear
    _columns = {
        #Nombre de la columna
        'name': fields.char ('Name', size = 128, required = True, select = True),
        'code': fields.char ('Code', size = 32, required =  True),
        'description' : fields.text('Description'),
        'session_ids' : fields.one2many('lesmed.course.session', 'course_id',string = 'Sessions'),
        'student_ids' : fields.many2many('res.partner', string = 'Students', domain=[('student','=', 'True')]),
        'teacher_id' : fields.many2one('res.users', string='Teacher', ondelete= 'set null', select = True),
        'total_seats': fields.integer('Total seats', required = True,),
        'available_seats' : fields.function(get_seats ,multi='seats' ,type = 'integer',string = 'Available seats', readonly = 'True'),
        'occupied_seats' : fields.function(get_seats, multi = 'seats',type = 'integer',string = 'Ocuppied seats', readonly = 'True'),
        'occupation_percentage' : fields.function(get_seats, multi='seats', type='float', string = 'Percentage of occupation', readonly = 'True', digits = (4,2)),

        }
    _defaults = {
                 'teacher_id': (lambda self,cr, uid, ids, context = {}: uid),
                 'total_seats': 20, 
                 
                 
                 }
    _sql_constraints = [ ('total_seats_positive', 'CHECK(total_seats>= 0)', 'The course\'s total seats must be a positive number'),
                        
                        
                        ]
    _constraints= [
                   (check_seats, 'The course is full, you cannot add more students.', ['student_ids']),
                   (check_seats, 'You cannot set a total seats limit under the number if actual students.', ['total_seats'])
                   ]
    


class Partner (osv.Model):
    
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    _columns = {
        'student' : fields.boolean('Student'),
        'student_code' : fields.char ('Code', size = 32, required = True, select = True ),
        'birthday' : fields.date ('Birthday'),
        'course_ids': fields.many2many('lesmed.course', string = 'Courses'),
                
        }
    
    @api.multi
    def on_change_is_company(self,is_company,student):
        res = self.onchange_type(is_company)
        #res = {'value' : {}, 'domain':{}, 'warning':{}}
        if is_company & student:
            res['value'].update({'student':False})
            res['warning'].update({'title': "Companies cannot be students", 'message' : "You changed the partner type to company. We blanked the student checkbox."}),
                                                                                                                                                              
        return res
    

#
    
class CourseSession (osv.Model):
    _name = 'lesmed.course.session'
    
    
    '''
    #version 7
    def approve(self, cr, uid, ids, context = {}):
        self.write(cr, uid, ids,{'state' : 'pending'}, context = context )
        return True
       ''' 
    #version 8
    @api.multi
    def button_approve(self):
        self.state = 'pending'
        return True
    @api.multi
    def button_start(self):
        self.state = 'open'
        return True
    @api.multi
    def button_done(self):
        self.state = 'done'
        return True
    @api.multi
    def button_cancel(self):
        self.state = 'canceled'
        return True
    @api.multi
    def button_reset(self):
        self.state = 'draft'
        return True
    
    
    
    
    @api.multi
    def get_end_time(self, field_names, arg):
        res= {}
        for session in self:
            end_time = (datetime.strptime(session.start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours = session.duration))
            res[session.id] = datetime.srtftime(end_time, '%Y-%m-%d %H:%M:%S')
            return res
    
        

        
        
    _columns = {
        'subject' : fields.char('Subject', size=256, required = True , select = True, readonly = True, states = {'draft':[('readonly', False)]}),
        'start_time': fields.datetime('Start time', requiered = True),
        'end_time' : fields.datetime ('End time'),
        'course_id': fields.many2one('lesmed.course',string ='Course', required = True, select = True, ondelete = 'cascade'),
        'state': fields.selection([('draft','Draft'), ('pending','Pending'), ('open','Open'), ('done', 'Done'), ('cancelled', 'Cancelled')],
                                  string = "State", select= True, required = 'True'),
                
        'teacher_id' : fields.related('course_id', 'teacher_id', type="many2one", relation = 'res.users',string = "Teacher", readonly = "True"),
        
        'occupied_seats' : fields.related('course_id','occupied_seats' ,type = "float", relation = 'res.users', string = 'Expected students', readonly = "True"),
        'duration' : fields.float('Duration', digits = (2,1), states = {'draft': [('readonly', False)]}),
        
                }
    _rec_name ='subject'
    _order = 'start_time'
     
    _defaults = {
                 'state' : 'draft'
                 
                 }
    
    
    
    
    