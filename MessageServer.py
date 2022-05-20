import os
import socket
from time import sleep
import sys

def registerUser(user):
    lines = []
    with open(completeName) as f:
        lines = f.readlines()
    count = 0
    addList = True
    for line in lines:
        count += 1
        if (line[:user.find("@")].strip() == user[:user.find("@")]):
            addList = False
            break
    if (addList):
        file = open(completeName, "a")
        file.write( user + "\n")
    return(addList)



inputFromUser = sys.argv[1]
serverURL = inputFromUser[:inputFromUser.find(":")].strip()
serverPort  = inputFromUser[inputFromUser.find(":") + 1:].strip()


os.mkdir(serverURL)

path = os.path.dirname(os.path.realpath(__file__))+"/"+serverURL


completeName = os.path.join(path, "userlist.txt")

file = open(completeName, "a")
file.close()



while(True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((serverURL, int(serverPort)))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                decodedData = data.decode()
                if(decodedData[:decodedData.find(" ")] == "POST"):
                    splietedData = decodedData[ decodedData.find("<p>") + 3 : decodedData.find("</p>") ].split()
                    if(splietedData[0] == "REGISTER"):
                        if (len(splietedData) > 2 or splietedData[1].count(":")> 1 or splietedData[1].count("@")> 1):
                            request="HTTP/1.1 INVALID USERNAME\r\n"
                        elif(registerUser(splietedData[1][:splietedData[1].find("@")+ 1]+ str(addr[0]) +":" + str(addr[1]))):
                            request="HTTP/1.1 200 OK\r\n"
                        else:
                             request="HTTP/1.1 INVALID USERNAME\r\n"
                        conn.send(request.encode())
                elif(decodedData[:decodedData.find(" ")] == "GET"):
                    splietedData = decodedData[ decodedData.find("<p>") + 3 : decodedData.find("</p>") ].split()
                    if(splietedData[0] == "userList"):
                        file = open(completeName, "r")
                        data = file.read()
                        conn.send(data.encode())
                        file.close()





 