from socket import *

#wrap the user input as http request and return string
def generateHTTP(x):
    re = 'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nAccept: text/html\r\nAccept-Language: us-en, fr, cn\r\n\r\ncmd=' + x
    return re
#unwrap the response msg from http format
def unwrap(x):
    modified_msg = x.decode() #decode from bytes
    output = modified_msg.split('HTTP/1.1 200 OK \r\n')
    #print(output[-1])
    return output[-1]

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while 1:
    input_check = input()
    sentence = generateHTTP(input_check)
    sen_byte = str.encode(sentence)
    clientSocket.send(sen_byte)
    modifiedSentence = unwrap(clientSocket.recv(1024))
    print(modifiedSentence)
    if(input_check == 'quit'):
        clientSocket.close()
        break
