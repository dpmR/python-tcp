#imports
import socket
import os
import time
import sys

#Variables
port = 4711
lHost = "127.0.0.1"

#Functions

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def send(msg):
    msg = str(msg)
    clientsocket.send(msg.encode("UTF-8"))
    print("Sent: " + msg)

def sendFile(filename):
    f = open(filename,'rb')
    print('Sending...')
    send("$")
    l = f.read(1024)
    while (l):
        print('Sending...')
        clientsocket.send(l)
        l = f.read(1024)
    f.close()
    send("!")
    print("Done Sending")
    #s.shutdown(socket.SHUT_WR)

def getFile(filename):
    f = open(filename,'wb')
    start_ctrl = clientsocket.recv(1)
    if start_ctrl == "$": 
        print("Receiving...")
        l = clientsocket.recv(1024)
        run = True
        while (run):
            print("Receiving...")
            f.write(l)
            l = clientsocket.recv(1024)
            if l[-1:] == "!" or l == "":
                print("Done Receiving")
                run = False
        f.close()
        print("File saved!")
        #clientsocket.send('Thank you for connecting')

#Starting Server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostname()
#host = lHost
serversocket.bind((host, port))
serversocket.listen(1)

clear()
print("-:-:-:-:-: Server:-:-:-:-:-")
clientsocket, addr = serversocket.accept()
print("Connection from: " + str(addr))
mode = "normal"
filename = ""
filename = ""

while True:
    print("Mode: " + mode)
    if mode == "normal": 
        #msg = str.strip(raw_input("Your Instruction: "))
        msg = str.strip(raw_input("Your Instruction: "))
    
        if msg == "help":
            clear()
            print("-+-+-+-+-+HELP+-+-+-+-+-")
            print("Test Connection: 'test'")
        
            raw_input("\nPress ENTER to continue")
            clear()
            print("-:-:-:-:-:Server:-:-:-:-:-")
                
        elif msg == "exit":
            mode = "exit"
        else:
            msg = msg.encode("UTF-8")
            mode == "normal"

            #send(msg)
            #clientsocket.shutdown(socket.SHUT_WR)        
            print(msg[12:])  
            if msg[0:11] == "getFileSize":
                print(msg[12:])
                filename = msg[12:]
                send("getFileSize " + filename)
                mode = "filesize"     
            elif msg[0:7] == "getFile":
                filename = msg[8:]
                print(filename)
                send("sendFile " + filename)
                mode = "getFile"
                print("switched mode to " + mode)
            elif msg[0:8] == "sendFile":
                filename = msg[9:]
                print(filename)
                send("getFile " + filename)
                mode = "sendFile"
                print("switched mode to " + mode)
            elif msg == "executeFile":
                print(msg[12:])
                file = msg[12:]
                send("executeFile " + file)
                mode = "exef"              
            elif msg[0:10] == "executeCmd":
                print(msg[11:])
                cmd = msg[11:]
                send("executeCmd " + cmd)
                mode = "exec" 
            else:
                send(msg)
                answer = clientsocket.recv(4096)
                if answer == "WC":
                    print("REC: WC (Wrong Command)")
                else: 
                    print(answer.decode("UTF-8"))

    elif mode == "getFile":
        getFile(filename);
        mode = "normal"
        print("switched mode to " + mode)

    elif mode == "sendFile":
        sleepTime = 1
        time.sleep(sleepTime)
        sendFile(filename)
        mode = "normal"
        print("switched mode to " + mode)

    elif mode == "exit":
        clientsocket.shutdown(socket.SHUT_RDWR)
        serversocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()
        serversocket.close()
        sys.exit()
        mode = "normal"
        print("switched mode to " + mode)

    elif mode == "exec" or mode == "exef":
        msg = clientsocket.recv(4096)
        print(msg)
        mode = "normal"
        print("switched mode to " + mode)

    elif mode == "filesize":
        msg = clientsocket.recv(4096)
        print("filesize: " + msg)
        mode = "normal"
        print("switched mode to " + mode)
        
    else:
        msg = clientsocket.recv(4096)
        mode = "normal"
        print("switched mode to " + mode)

