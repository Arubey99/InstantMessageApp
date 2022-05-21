# InstantMessageApp

>Python program that is an instant messaging application which uses a server to register and to find addresses of the other users, and a peer-to-peer connection to send and receive messages directly to other users. Between the client and server program uses TCP protocol and between the client to client it uses UDP protocol.

## Program Algorithm 

### MessageServer:


![image](https://user-images.githubusercontent.com/67705318/169646694-1929286c-c8a8-4421-b5c0-86045a550661.png)

When registerUser function called the past used added to the userlist.txt file. If username already in the list the program brakes.

![image](https://user-images.githubusercontent.com/67705318/169646758-f0c878e1-54c4-4a14-a9d5-5922733d0dc7.png)


In these lines program get input from the user from console and find the path of the folder. Than create new folder with the IP address of the server and in that server program creates a txt file with name userlist.

![image](https://user-images.githubusercontent.com/67705318/169646918-d5853f00-58a0-4d2f-99fe-2a2a088ce62c.png)


In the above code the program enters an infinite loop and waits for the tcp connection. If the tcp connection is established programs looks for the “Get” or “Post” message in the message. If it gets “POST” and the massage contains REGISTER it then looks for the invalid characters in the name and send error message to the client and if there aren’t any invalid characters in the name server registers the server to the userlist.txt file. If the server gets the “Get” server sends the userlist.txt to the client and close the connection. 


### InstantMessager:

userList = []

![image](https://user-images.githubusercontent.com/67705318/169646997-ee500cac-70d3-45a6-bb87-bb9da0b182d5.png)

Prgoram creates a local userList and gets the hostIP, host port and mode from the console.

![image](https://user-images.githubusercontent.com/67705318/169647024-7c4a511b-0078-4a84-954f-7c4b3d9531d4.png)

If updateList function called the local userList list is updated using TCP connection with the server.

![image](https://user-images.githubusercontent.com/67705318/169647032-1372a662-f86d-4aae-ad22-c7feb8cf2596.png)

In printList function client updates its local user list and prints every element in this list.


![image](https://user-images.githubusercontent.com/67705318/169647042-cd759d12-9334-494b-b0a7-dde8cf4bb335.png)

Looks for the entered username in the local List. The local list would be updeated before this function is called so there is no need to call updateList function.

![image](https://user-images.githubusercontent.com/67705318/169647061-af213b25-f1a5-4704-8b86-1807209c14ba.png)

In sendUDPmessage the passed message send to the entered ID and port.

![image](https://user-images.githubusercontent.com/67705318/169647135-caf7c670-a942-412e-95c0-e97cdab616cf.png)

In findUserIp the entered username is searched in the userList and return IP:PORT if the username not found returns -1.

![image](https://user-images.githubusercontent.com/67705318/169647146-5ea69a72-43e3-48c0-868b-6fe42a38b2a2.png)

In sender function first function looks for the enterd IP in the userList using findUserIp function then if no user finds print user not found message and if the user found it sends the message to the that username.

![image](https://user-images.githubusercontent.com/67705318/169647174-e634ccce-aac0-4dbf-a51a-ff8bcac3a994.png)

If user enters Listen the program enters Listen mode and send the username to the server to register itself. If the user enters invalid username the program enters a loop to user enter valid username.  After that program enters infinite loop and waits for the messages. After message entered the program prints the massage with the username and wait for the new messages.

![image](https://user-images.githubusercontent.com/67705318/169647184-591590db-21e8-453e-8a75-eb2a08b8097f.png)

If the user enters send as a user program first updates its local user list and waits for inputs. If user enters exit the program closes. If the program enters list program calls updateList function and prints the list. If the user inputs unicast program updates its userList and try to send the entered message to the entered user. If user inputs multicast it creates a list that contains entered users and using for loop send message to the entered users by calling sender function. If user enters broadcast program updates its local userList and send all the users in the userList entered message. 

The program uses UDP communication between the client-to-client communication and uses TCP communication between the server and client.
