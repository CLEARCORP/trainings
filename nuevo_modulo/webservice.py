import xmlrpclib

username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'trainings'    #the database

server = 'localhost'
port = '8069'

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://%s:%s/xmlrpc/common' % (server, port))
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/object' % (server, port))

course_ids = sock.execute(dbname, uid, pwd, 'nuevo_modulo.course', 'search', [('code','=','TTT')])
courses = sock.execute(dbname, uid, pwd, 'nuevo_modulo.course', 'read', course_ids, ['code', 'name'])
res = sock.execute(dbname, uid, pwd, 'nuevo_modulo.course', 'write', course_ids, {'code': 'TTT'})
res = sock.execute(dbname, uid, pwd, 'nuevo_modulo.course', 'check_seats', course_ids)

print res