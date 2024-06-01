import socket 
import threading
#from _thread import *
names = []
currentsender = ''
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    def __init__(self):
        self.store = [None for _ in range(16)]
    def get(self, key):
        index = hash(key) & 15
        if self.store[index] is None:
            return None
        n = self.store[index]
        while True:
            if n.key == key:
                return n.value
            else:
                if n.next:
                    n = n.next
                else:
                    return None
    def put(self, key, value):
        nd = Node(key, value)
        index = hash(key) & 15
        n = self.store[index]
        if n is None:
            self.store[index] = nd
        else:
            if n.key == key:
                n.value = value
            else:
                while n.next:
                    if n.key == key:
                        n.value = value
                        return
                    else:
                        n = n.next
                n.next = nd
hm = HashMap()

class serverside:
    clients_list = []    
    recentmssg = ""
    def __init__(self):
        self.serversocket = None
        self.broadcast = True
        self.createserver()
    def createserver(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket using TCP port and ipv4
        local_ip = '127.0.0.1'
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.serversocket.bind((local_ip, local_port))
        print("server is listening for incoming messages..")
        self.serversocket.listen(5) #listen for incomming connectionss max 5 clients
        self.start_in_a_new_thread()
    def broadcast1(self,so):
        self.broadcast = False
    def receivemssg(self,so):
        while True:
            incomingbuffer = so.recv(13) #data
            if not incomingbuffer:
                break
            self.recentmssg = incomingbuffer.decode('utf-8')
            parsedmessage = self.recentmssg.splitlines()
            check = int(parsedmessage[1])
            length1 = len(parsedmessage[2])
            #print(check)
            #print(parsedmessage[0])
            a = "@all"
            if check > length1 :
                self.sendtosameclient1(so)
                self.broadcast1(so)
                so.close()                
            elif parsedmessage[0] == a:
                self.recentmssg = parsedmessage[2]
                self.sendtoallclient(hm.get(so),so)
                self.deliverymessage(so)
                print('messageforwardedtoclient')
            elif parsedmessage[0] in names and check <= 13:
                self.recentmssg = parsedmessage[2]
                self.sendtoaspecifiedclient(hm.get(so),hm.get(parsedmessage[0])) 
                self.deliverymessage(so)
                print('message forwarded to '+ parsedmessage[0][1:])
            else:
                self.sendtosameclient(so)
            #print(self.recentmssg)
        so.close()
    def deliverymessage(self,so):
        so.send('messagedeliveredsuccessfully'.encode('utf-8'))
    def sendtosameclient(self,so):
        so.send('ERROR102 Unable to send'.encode('utf-8'))
    def sendtosameclient1(self,so):
        so.send('ERROR103 Headerincomplete'.encode('utf-8'))
    def sendtoaspecifiedclient(self,name,so):
        mes = 'message recieved from '+ name[1:] +':'+self.recentmssg
        so.send(mes.encode('utf-8'))
    def sendtoallclient(self,name,so):
        for client in self.clients_list:
            socket1, (ip, port) = client
            if socket1 is not so:
                if self.broadcast == True:
                    mes1 = 'broadcasted message from '+ name[1:] +':'+self.recentmssg
                    socket1.sendall(mes1.encode('utf-8'))
                else:
                    break
    def start_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.serversocket.accept()
            self.add_to_clients_list(client)
            so.send('NICK'.encode('utf-8'))
            nickname = so.recv(1024).decode('utf-8')
            if nickname == '':
                print('ERROR101 No user registered')
            if nickname.isalnum():
                so.send('registered successfully'.encode('utf-8'))
                names.append('@'+nickname)
                hm.put('@'+nickname,so)
                hm.put(so,'@'+nickname)
                #print(client)
                print(nickname + ' registered in server')
                t = threading.Thread(target=self.receivemssg, args=(so,))
                t.start()
            else:
                so.send('ERROR 100 Malformed username'.encode('utf-8'))
            #hm.put(name,so)
    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)

if __name__ == "__main__":
    serverside()
                