from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("user","12345","/home/",perm="elradfmw")
authorizer.add_anonymous("/home/shiyanlou")

handler = FTPHanler
handler.authorizer = authorizer
handler.passive_ports = range(2000,2333)

server = FTPServer(("127.0.0.1",21),handler)
server.server_forever()
