from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 6789


serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("the web server is up on: localhost:6789")
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        print("Ready to serve...")
        message = connectionSocket.recv(1024)
        message.decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputData = f.read()

        message0 = "\nHTTP\1.1 200 OK\n"
        connectionSocket.send(message0.encode())
        for i in range(0, len(outputData)):
            connectionSocket.send(outputData[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        message1 = "\nHTTP\1.1 404 Not Found\n"
        print("Inside Exception")
        connectionSocket.send(message1.encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()

