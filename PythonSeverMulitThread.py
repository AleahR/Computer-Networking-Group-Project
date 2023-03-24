from socket import *
import threading
import sys

class ClientThread(threading.Thread):
    def __init__(self, connect, address):
        threading.Thread.__init__(self)
        self.connectionSocket = connect
        self.addr = address
    def run(self):
        while True:
            try:
                message = connectionSocket.recv(1024)
                if not message:
                    break
                print ("message: \n", message)
                filename = message.split()[1]
                f = open(filename[1:])
                outputdata = f.read() 
                print ("outputdata:", outputdata)
                header1 = "HTTP/1.1 200 OK"
                header_info = {
                    "Content-Length": len(outputdata),
                    "Keep-Alive": "timeout=%d,max=%d" %(10,100),
                    "Connection": "Keep-Alive",
                    "Content-Type": "text/html"
                    }

                header2 = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
                print ("second_header:", header2)
                connectionSocket.send(("%s\r\n%s\r\n\r\n" %(header1, header2)).encode())
                for i in range(0, len(outputdata)):
                    connectionSocket.send(str.encode(outputdata[i]))
                connectionSocket.send(("\r\n").encode())
            except IOError:
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                #connectionSocket.send(("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n").encode()) 
                #connectionSocket.close()

if __name__ == '__main__':
    serverSocket = socket(AF_INET, SOCK_STREAM) 
    serverPort = 6788
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    threads=[]
    while True:
        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()
        print("addr:\n", addr)
        client_thread = ClientThread(connectionSocket,addr)
        client_thread.setDaemon(True)
        client_thread.start()
        threads.append(client_thread)
    serverSocket.close()
    sys.exit()