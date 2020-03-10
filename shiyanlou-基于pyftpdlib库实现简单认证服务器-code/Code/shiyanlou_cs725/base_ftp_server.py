import logging

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import ThrottledDTPHandler, FTPHandler
from pyftpdlib.servers import FTPServer

from config_ftp import *

def init_ftp_server():
    authorizer = DummyAuthorizer()
    """
            read :
            - "e" = change file list
            - "l" = list files
            - "r" = receive file from the server (RETR command)

            write :
            - "a" = upload file (APPE command)
            - "d" = delete file (DELE, RMD commands)
            - "f" = rename the file (RNFR, RNTO commands)
            - "m" = create file (MKD command)
            - "w" = write (STOR, STOU commands)
            - "M" = transfer file MOD (SITE CHMOD command)
    """
    if enable_anonymous:
        authorizer.add_anonymous(anonymous_path)

    for user in user_list:
        name,passwd,permit,homedir = user
        try:
            authorizer.add_user(name,passwd,homedir,perm=permit)
        except:
            print("there're some wrong in the base_ftp.ini ")
            print(user)
    dtp_handler = ThrottledDTPHandler

    dtp_handler.read_limit = max_download
    dtp_handler.write_limit = max_upload

    handler = FTPHandler
    handler.authorizer = authorizer

    if enable_logging:
        logging.basicConfig(filename='pyftp.log',level=logging.INFO)

    handler.banner = welcome_banner
    handler.masquerade_address = masquerade_address

    handler.passive_ports = range(passive_ports[0],passive_ports[1])

    address = (ip, port)
    server = FTPServer(address, handler)

    server.max_cons = max_cons
    server.max_cons_per_ip = max_pre_ip

    server.serve_forever()

def ignor_octothrpe(text):
    for x, item in enumerate(text):
        if item == "#":
            print(text[:x])
            return text[:x]
        pass
    print(text)
    return text

def init_user_config():
    f = open("baseftp.ini",encoding='utf-8')
    while 1:
        line = f.readline()
        if len(ignor_octothrpe(line)) > 3:
            print(line.split())
            user_list.append(line.split())
            # todo
        if not line:
            break

if __name__ == '__main__':
    user_list = []
    init_user_config()
    init_ftp_server()
"""
authorizer.add_user("user","12345","/home/",perm="elradfmw")
authorizer.add_anonymous("/home/shiyanlou")

handler = FTPHandler
handler.authorizer = authorizer
handler.masquerade_address = '192.168.43.181'
handler.passive_ports = range(2000,2333)

server = FTPServer(("127.0.0.1",21),handler)
server.serve_forever()
"""

