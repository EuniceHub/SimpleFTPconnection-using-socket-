from socket import *

#the function is to unwrapped the messaged sent in http request form and return in string
def decode_http(a):
    decode_org = a.decode("utf-8") #decode from bytes into bytes
    decode_msg = decode_org.split('\r\n')
    decode_msg = decode_msg[-1][4:]
    msg_bytes = str.encode(decode_msg)
    return msg_bytes

#wrap up the http response with in http response and return the msg in bytes
def httpresponse(b):
    #translate from bytes into string
    org = b.decode()
    modified_msg = 'HTTP/1.1 200 OK \r\n' + org
    print(modified_msg)
    encode_msg = str.encode(modified_msg) #translate into bytes from string
    return encode_msg


    
    
serverPort = 12000
#finalserver = 'ftp.cdc.gov'
serverSocket = socket(AF_INET,SOCK_STREAM)#the socket connect with client
#ftpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
#ftpSocket.connect((finalserver, ftpPort))
serverSocket.listen(3)
print('The server is ready to receive')
conn, addr = serverSocket.accept()
message = conn.recv(1024) #receive the msg from user input
msg1 = decode_http(message) #extract the ftp command
cmd = msg1.split()[0].decode()
addr1 = msg1.split()[1].decode()
ftpSocket=socket(AF_INET, SOCK_STREAM)
ftpSocket.connect((addr1, 21))
usercheck = 0 #state for checking username
passcheck = 0 #state for checking password
while 1:
    if cmd == 'ftp':
        print('connect with ftp server')
        response = ftpSocket.recv(1024)
        conn.sendall(httpresponse(response))
        usercheck = 1
        #cmd = conn.recv(1024)
        #conn.send(str.encode("username: "))
    elif usercheck == 1:
        #use = cmd.decode() #decode string
        username = 'user ' + cmd + '\r\n'
        cmd_byte = str.encode(username)
        ftpSocket.sendall(cmd_byte)
        response1 = ftpSocket.recv(1024) #in bytes
        response2 = httpresponse(response1)
        conn.sendall(response2)
        passcheck = 1
        usercheck = 0
    elif passcheck == 1:
        cmd = 'pass ' + '\r\n'
        cmd_byte = str.encode(cmd)
        ftpSocket.sendall(cmd_byte)
        response1 = ftpSocket.recv(1024) #in bytes
        conn.sendall(httpresponse(response1))
        passcheck = 0
    else:
        pass_cmd = cmd + '\r\n'
        cmd_byte = str.encode(pass_cmd)
        ftpSocket.sendall(cmd_byte)
        response1 = ftpSocket.recv(1024) #in bytes
        conn.sendall(httpresponse(response1))
        if(cmd == 'quit'):
            conn.close()
            break
        
    next_cmd = conn.recv(1024)
    cmd_string = decode_http(next_cmd) #ftp cmd in string
    cmd = cmd_string.decode("utf-8") #ftp cmd in bytes
    print(cmd)
    
