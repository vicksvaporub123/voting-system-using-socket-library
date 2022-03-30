from socket import *
import time as t
import json
import matplotlib.pyplot as plt
from os import system, name
import math

def clear():

	# for windows
	if name == 'nt':
		_ = system('cls')

	# for mac and linux(here, os.name is 'posix')
	else:
		_ = system('clear')

serv_or_client = input("Enter 1 to run as server, anything else to run as client: ")

if(serv_or_client == '1'):
    parties = ""
    num_part = 0
    voting_system = {}

    num_part = int(input("Enter number of parties:"))
    for i in range(num_part):
        parties = input('Enter party:')
        voting_system[parties] = 0
    serverPort = 12001
    print("Dictionary created with party names")
    print(voting_system)
    servername = gethostname()
    ip=gethostbyname(servername)
    print("The server is listening on IP address:",ip)
    #print(servername)
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    #print ('The server is ready to receive')

    '''w = connectionSocket.recv(1024)
    w = w.decode()'''

    #if(w == "1"):
    
    connectionSocket, addr = serverSocket.accept()
    print("Connection established")
    while(1):
        #vote = json.dumps(voting_system).encode('utf-8')
        vote = str(voting_system)
        vote = str.encode(vote)
        connectionSocket.send(vote)
        sentence = connectionSocket.recv(1024)
        sentence = sentence.decode()
        if(sentence == '200'):
            continue
        else :
            if(sentence == 'disp'):
                n2 = str(voting_system)
                n2 = str.encode(n2)
                connectionSocket.send(n2)
            else :
                voting_system[sentence]+=1
                capitalizedSentence = sentence.upper()
                s2 = 'Vote has been counted'
                s2 = str.encode(s2)			
                connectionSocket.send(s2)
            temp = connectionSocket.recv(1024)
            temp = temp.decode()
            #print(temp)
            if temp == '0':
                strdict = str(voting_system)
                diction = str.encode(strdict)
                connectionSocket.send(diction)
                connectionSocket.close()
                print("Connection closed")
                break
            else:
                continue

else:
    serverName = input("Enter IP address to connect to:")
    serverPort = 12001
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print("Connection established")
    temp = 1
    while(temp!='0'):
        print("Options:")
        option = clientSocket.recv(1024)
        #option = json.loads(option.decode('utf-8'))
        option = option.decode()
        op2 = eval(option)
        loption = []
        for i in op2.keys():
            loption.append(i)
        for i in loption:
            print(i)
        sentence = input("Which party would you like to vote for?\n")
        if sentence not in loption :
            print('Enter valid party name.')
            errmsg = '200'
            errmsg = str.encode(errmsg)
            clientSocket.send(errmsg)
            t.sleep(2)
            clear()
        else :
            sentence = str.encode(sentence)
            clientSocket.send(sentence)
            modifiedSentence = clientSocket.recv(1024)
            print ('From Server: ', modifiedSentence.decode())

            temp = input('Enter 0 to exit, anything else to accept more votes: ')
            temp = str.encode(temp)
            #print(temp)
            clientSocket.send(temp)
            temp = temp.decode()
            clear()
            if temp == '0':
                results = clientSocket.recv(1024)
                results = results.decode()
                #res2 = eval(results)
                res2 = eval(results)
    wc = 0
    for i in res2.keys():
        if(res2[i] == max(res2.values())):
            wc+=1
            print("Winner(s) are",i)
    if(wc > 1):
        print("There are",wc,"parties with same number of votes\n")
    part = res2.keys()
    votes = res2.values()
    count = range(math.floor(min(votes)), math.ceil(max(votes))+1)
    #fig = plt.figure(figsize = (10, 5))
    yint = range(min(count), math.ceil(max(count))+1)
    plt.yticks(yint)
    plt.bar(part,votes,width = 0.4)
    plt.xlabel("Party name")
    plt.ylabel("Number of votes received")
    plt.title("Vote Distribution")
# show plot
    plt.show()
    print("Connection closed")
    clientSocket.close()
    #if temp == 0:
    
    #clientSocket.close()
