from ast import Global
import socket
from time import sleep
import sys
import socket

userList = []

inputFromUser = sys.argv
userName = sys.argv[1].strip()
HOST = sys.argv[2][:(sys.argv[2]).find(":")].strip()
PORT = sys.argv[2][(sys.argv[2]).find(":") + 1:].strip()
PORT = int(PORT)
mode = sys.argv[3].strip()



def updateList():
    global userList 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request="GET " + "serverURL/userlist.txt" + " HTTP/1.1\r\n" + "<html><body>\n <p>" + "userList " +"</p>\n"+  "</html></body>\n"
        s.send(request.encode())
        data = s.recv(1024)
        decodedData = data.decode()
        userList = decodedData.split()

def printList():
    global userList
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request="GET " + "serverURL/userlist.txt" + " HTTP/1.1\r\n" + "<html><body>\n <p>" + "userList " +"</p>\n"+  "</html></body>\n"
        s.send(request.encode())
        data = s.recv(1024)
        decodedData = data.decode()
        userList = decodedData.split()
        if userList != []:
            print("The online users are:")
        for element in userList:
            print(element[:element.find("@")])

def findUser(name):
    global userList
    for element in userList:
        nameCompare = element[:element.find("@")]
        if (name == nameCompare):
            return element[element.find("@") + 1 :]
    return "-1"


def sendUDPmessage(UDP_ID, UDP_PORT, message):
    global userList
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message=userName+ " HTTP/1.1\r\n" + "<html><body>\n <p>" +message + "</p>\n"+  "</html></body>\n"
        encodedMessage = message.encode()
        s.sendto(encodedMessage,(UDP_ID,int(UDP_PORT)))

def findUserIp(inputName):
    global userList
    for element in userList:
        elementSliced = (element[:element.find("@")])
        if (inputName == elementSliced):
            return element[element.find("@") + 1 :]
    return "-1"

def sender(sendUserName, message):
    global userList
    sendUserIsFind= findUser(sendUserName)
    if (sendUserIsFind.strip() != "-1"):
        sendUserIP = findUserIp(sendUserName)
        UDP_ID = sendUserIP[:sendUserIP.find(":")]
        UDP_PORT = sendUserIP[sendUserIP.find(":")+1 :].strip()
        sendUDPmessage(UDP_ID, UDP_PORT, message)
        print("message is sent to " + sendUserName)
    else:
        print("user " + sendUserName + " not found")


if(mode == "listen"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request="POST " + "serverURL/userlist.txt" + " HTTP/1.1\r\n" + "<html><body>\n <p>" + "REGISTER " + userName + "@"+str(HOST)+":"+str(PORT) +"</p>\n"+  "</html></body>\n"
        s.send(request.encode())
        data = s.recv(1024)
        decodedData = data.decode()
        while(decodedData.strip() == "HTTP/1.1 INVALID USERNAME"):
            print("INVALID USERNAME")
            userName = input("Enter User Name:") 
            request="POST " + "serverURL/userlist.txt" + " HTTP/1.1\r\n" + "<html><body>\n <p>" + "REGISTER " + userName + "@"+str(HOST)+":"+str(PORT) +"</p>\n"+  "</html></body>\n"
            s.send(request.encode())
            data = s.recv(1024)
            decodedData = data.decode()
        request="GET " + "serverURL/userlist.txt" + " HTTP/1.1\r\n" + "<html><body>\n <p>" + "userList " +"</p>\n"+  "</html></body>\n"
        s.send(request.encode())
        data = s.recv(1024)
        decodedData = data.decode()
        userList = decodedData.split()
        thisUser = ((userList[-1])[userList[-1].find("@") + 1 :]).split(":")
        serverURL = thisUser[0]
        serverPort = thisUser[1]
        s.close()
        
        
        while(True):
            UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            UDPServerSocket.bind((serverURL, int(serverPort)))
            while True:
                bytesAddressPair = UDPServerSocket.recvfrom(1024)
                decodedData = bytesAddressPair[0].decode()
                name = decodedData [:decodedData.find(" ")]
                splietedMessage = decodedData[ decodedData.find("<p>") + 3 : decodedData.find("</p>") ].strip()

                print(name + ": " + splietedMessage)
                
           

if(mode == "send"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request="GET " + "serverURL/userlist.txt" + " HTTP/1.1\r\n" + "<html><body>\n <p>" + "userList " +"</p>\n"+  "</html></body>\n"
        s.send(request.encode())
        data = s.recv(1024)
        
        decodedData = data.decode()
        userList = decodedData.split()
        s.close()
        userChoice = " "

        while (userChoice != "exit"):
            
            userInput = input()
            if(userInput.strip().lower() == "exit"):
                break
            elif(userInput.strip().lower() == "list"):
                printList()
            else:
                userChoice = userInput[:userInput.find(" ") + 1]
                userChoice = userChoice.lower()
                userInput = userInput[userInput.find(" ") + 1 :]
                if(userChoice.strip() == "unicast"):
                    updateList()
                    sendUserName = userInput[:userInput.find(" ")]
                    message = userInput[userInput.find("“") + 1 : userInput.find("”")]
                    sender(sendUserName,message)
                elif(userChoice.strip() == "multicast"):
                    updateList()
                    userNames = userInput[userInput.find("[") + 1 : userInput.find("]")]
                    userNames = userNames.strip().split(",")
                    message = userInput[userInput.find("“") + 1 : userInput.find("”")]
                    for user in userNames:
                        sender(user, message)

                elif(userChoice.strip() == "broadcast"):
                    updateList()
                    message = userInput[userInput.find("\"") + 1 :]
                    message = message[:message.find("\"") :]
                    for user in userList:
                        name = user[:user.find("@")]
                        sender(name, message)

                





