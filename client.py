#Imports
import socket
import time
import random
import subprocess

#Variables
lHost = "127.0.0.1"            #Server IP
port = 4711			           #Connection Port
filename_inc = ""
filename_out = ""

#Functions

def send(msg):
    s.send(msg.encode("UTF-8"))
    print("Sent: " + msg)

def sendFile(filename):
    f = open(filename,'rb')
    print('Sending...')
    send("$")
    l = f.read(1024)
    while (l):
        print('Sending...')
        s.send(l)
        l = f.read(1024)
    f.close()
    send("!")
    print("Done Sending")
    #s.shutdown(socket.SHUT_WR)
    #print s.recv(1024)

def getFile(filename):
    f = open(filename,'wb')
    start_ctrl = s.recv(1)
    if start_ctrl == "$": 
        print("Receiving...")
        l = s.recv(1024)
        run = True
        while (run):
            print("Receiving...")
            f.write(l)
            l = s.recv(1024)
            if l[-1:] == "!" or l == "":
                print("Done Receiving")
                run = False
        f.close()
        print("File saved!")
        #clientsocket.send('Thank you for connecting')
    
def getInstructions():
    connected = True

    while (connected):
        msg = s.recv(4096)
        inst = msg.decode("UTF-8")
        
        #Instructions        
        if inst == "test":
            try:
                print("REC: test")
                send("[OK]Test works!")
            except:
                pass

        elif inst == "ping":
            try:
                print("REC: ping")
                send("pong")
            except:
                pass

        elif inst[0:8] == "sendFile":
            print("REC: sendFile")
            try:
                print(inst[9:])
                filename_out = inst[9:]
                print("sending file..")
                sleepTime = 1
                time.sleep(sleepTime)
                sendFile(filename_out)
            except:
                pass

        elif inst[0:7] == "getFile":
            print("REC: getFile")
            try:
                print(inst[8:])
                filename_inc = inst[8:]
                print("receiving file..")
                getFile(filename_inc)
            except:
                pass

        elif inst == "executeTop":
            print("REC: executeTop")
            try:
                print("executing top...")
                subprocess.Popen("top", shell=True)
            except:
                pass

        elif inst == "executeFile":
            print("REC: executeFile")
            try:
                print("executing file...")
                subprocess.Popen("./client.py", shell=True)
            except:
                pass

        elif inst == "":
            connected = False

        else:
            print("wrong command:")
            print(msg)
            send("WC")
		
#Connection

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
#host = lHost
conn