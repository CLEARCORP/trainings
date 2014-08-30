import xmlrpclib

username = 'admin'
password = 'admin'
database = 'trainings'
server = 'localhost'
port = '8069'

sock_common = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/common' % (server, port))
uid = sock_common.login(database, username, password)
sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/object' % (server, port))


course_ids = sock.execute(database, uid, password, 'cv_clearcorp.course', 'search', [('code','=','CTP-TEC')])
courses = sock.execute(database, uid, password, 'cv_clearcorp.course', 'read', course_ids, ['code', 'name'])
#res = sock.execute(database, uid, password, 'cv_clearcorp.course', 'write', course_ids, {'name': 'Odoo Technical Cert. Course'})
res = sock.execute(database, uid, password, 'cv_clearcorp.course', 'check_seats', course_ids)
print res