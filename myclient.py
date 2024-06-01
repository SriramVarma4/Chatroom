import socket #Sockets for network connection
import threading # for multiple proccess 
import sys

nickname = input("Choose your name: ")
class clientside:
    #clientsocket = None
    recentmssg = None
    
    def __init__(self):
        self.clientsocket = None
        self.initializesocket()
        self.listenforincomingmssg()
        self.sendmessage()
    def initializesocket(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialazing socket with TCP and IPv4
        remote_ip = '127.0.0.1'
        remote_port = 10319
        self.clientsocket.connect((remote_ip, remote_port)) #connect to the remote server
    def listenforincomingmssg(self):
        thread = threading.Thread(target= self.receivefromserver, args=(self.clientsocket,)) # Create a thread for the send and receive in same time 
        thread.start()
    def sendmessage(self):
        thread1 = threading.Thread(target= self.sendtoserver, args=(self.clientsocket,)) # Create a thread for the send and receive in same time 
        thread1.start()

    def receivefromserver(self,so):
        while True:
            try:
                buffer = so.recv(1024)
                if not buffer:
                    break
                message = buffer.decode('utf-8')
                if message == 'NICK':
                    so.send(nickname.encode('utf-8'))
                elif message == 'registered successfully':
                    print('registered successfully')
                elif message == 'ERROR 100 Malformed username':
                    print('ERROR 100 Malformed username')
                elif message == 'ERROR102 Unable to send':
                    print('ERROR102 Unable to send')
                    message = ''
                elif message == 'ERROR103 Headerincomplete':
                    print('ERROR103 Headerincomplete')
                    message = ''
                elif message == 'messagedeliveredsuccessfully':
                    print('messagesentsuccessfully')
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured client closed`!")
                so.close()
                break
    # Sending Messages To Server
    def sendtoserver(self,so):
        while True:
            message = input()
            modimssg = message.split(' ',1)
            length = len(modimssg[1])
            sendmssg = modimssg[0] + '\n' + str(length) + '\n' + modimssg[1]
            so.send(sendmssg.encode('utf-8'))
                
if __name__ == "__main__":
    clientside()
        