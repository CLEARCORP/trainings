# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

#las clases en python tienen que empezar con mayuscula en cada palabra
class Course (osv.Model):
    _name = 'lesmed.course'
    
    
    def get_seats(self, cr, uid,ids,field_name,arg,context={}):
        res = {} 
        courses = self.browse(cr,uid, ids, context = context)
        for course in courses:
            
            total_seats = course.total_seats
            
            students = course.student_ids
            
            occupied_seats = len(students)
            
            available_seats = total_seats  - occupied_seats
            res[course.id] ={
                               'available_seats' : available_seats,
                               'occupied_seats' : occupied_seats,
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
    
    #columnas de la tabla que se va a crear
    _columns = {
        #Nombre de la columna
        'name': fields.char ('Name', size = 128, required = True, select = True),
        'code': fields.char ('Code', size = 32, required =  True),
        'description' : fields.text('Description'),
        'session_ids' : fields.one2many('lesmed.course.session', 'course_id',string = 'Sessions'),
        
        'student_ids' : fields.many2many('lesmed.student', string = 'Students'),
        'teacher_id' : fields.many2one('res.users', string='Teacher', ondelete= 'set null', select = True),
        'total_seats': fields.integer('Total seats', required = True,),
        'available_seats' : fields.function(get_seats ,multi='seats' ,type = 'integer',string = 'Available seats', readonly = 'True'),
        'occupied_seats' : fields.function(get_seats, multi = 'seats',type = 'integer',string = 'Ocuppied seats', readonly = 'True'),
        
        
        
        
        
               }

class Student (osv.Model):
    _name = 'lesmed.student'
    
    _columns = {
        'name' : fields.char ('Name', size = 128, required = True, select= True),
        'code' : fields.char ('Code', size = 32, required = True, select = True ),
        'birthday' : fields.date ('Birthday'),
        'course_ids': fields.many2many('lesmed.course', string = 'Courses'),
                }
    
class CourseSession (osv.Model):
    _name = 'lesmed.course.session'
    _columns = {
        'subject' : fields.char('Subject', size=256, required = True , select = True),
        'start_time': fields.datetime('Start time', requiered = True),
        'end_time' : fields.datetime ('End time'),
        'course_id': fields.many2one('lesmed.course',string ='Course', required = True, select = True, ondelete = 'cascade'),
                }
    _rec_name ='subject'
    _order = 'start_time'
    
    
    
    
    
    