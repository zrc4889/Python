from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

authorizer = DummyAuthorizer()
authorizer.add_user('python', '123456', 'E:\\', perm='elradfmwM')
handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(('192.168.6.247', 2121), handler)
server.serve_forever()