import sys
import socket
import time

class Client():
    def __init__(self,host, port, mine_time):
        self.host = host
        self.port = port
        self.mine_time = mine_time
    def execute(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        startTime = time.time()
        currentTime = 0
        numKBSent = 0

        theDataSendFromClient = bytes(1000)

        while currentTime - startTime < (self.mine_time):
           
            client.sendall(theDataSendFromClient)
            numKBSent += 1
            currentTime   = time.time()

        client.close()

        rate = (numKBSent * 8.0) / (currentTime - startTime)
        rate = rate/1000 # kbps to mbps
        print("sent=",numKBSent, " KB rate=" , rate , " Mbps")
       


class Server():
    def __init__(self, mine_port):
        self.mine_port = mine_port

    def execute(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", self.mine_port))
        server.listen(10)
        print("[*] Listening on 127.0.0.1",":",self.mine_port)
        
        startTime = time.time()
        currentTime = 0
        client,addr = server.accept()
        total_data=[]
        while True:
            data = client.recv(1000)
            if len(data)==0:
                currentTime = time.time()
                break

            total_data.append(data)
        # print(currentTime,startTime,currentTime-startTime)
        numKBSent = len(total_data)
        rate = (numKBSent * 8.0) / (currentTime-startTime)
        rate = rate/1000 # kbps to mbps
        print("sent=",numKBSent, " KB rate=" , rate , " Mbps")


def main():
    i = 0
    arg = ""
    client = False
    clientOrServer = False
    time = 0
    port = 0
    host = ""

    args = sys.argv[1::]

    while i < len(args):

        if args[i] == "-s":
            if len(args) != 3:
                print("Error: missing or additional arguments")
                sys.exit()
            client = False
            clientOrServer = True
            break

        if args[i] == "-c":
            if len(args) != 7:
                print("Error: missing or additional arguments")
                sys.exit()
            client = True
            clientOrServer = True
            break

        i = i+1

    if clientOrServer == False:
        print("Error: missing or additional arguments")
        sys.exit()
    i = 0

    while i < len(args) and args[i][0] == "-":
        arg = args[i]
        i = i+1
        if arg[1] == "c" or arg[1] == "s":
            continue
       
        if arg[1] == 't':
            if (client):
                try:
                    
                    time = int(args[i])
                    i = i+1
                except:
                    print("Error: time must be an integer")
                    sys.exit()

            else:
                print("Error: missing or additional arguments")
                sys.exit()
                

        elif arg[1] == 'p':
            try:
                port = int(args[i])
                i = i+1
            except:
                print("Error: port number must be in the range 1024 to 65535")
                sys.exit()
            if (port <= 1024 or port >= 65535):
                print("Error: port number must be in the range 1024 to 65535")
                sys.exit()
            

        elif arg[1] == 'h':
            if (client):
            	host = args[i]
            	i=i+1
            else:
            	print("Error: missing or additional arguments")
            	sys.exit()

        else:
            print("Error: missing or additional arguments")

    if client:
	    tcpClient = Client(host, port, time)
	    tcpClient.execute()

    if client == False :
	    tcpServer = Server(port)
	    tcpServer.execute()
		
main()


#Iperfer -c -h <server hostname> -p <server port> -t <time>