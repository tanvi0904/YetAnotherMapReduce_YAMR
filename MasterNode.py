import threading
import json
import socket

def nodesdictwrite(n=2,filename="xyz"):
    a=dict()
    filename, file_extension = filename.split(".")
    for i in range(n):
        a[i]=["127.0.0.1",23333+i,filename+str(i)+"."+file_extension]
        connec=threading.Thread(target=w.conne,args=(a[i][0],a[i][1],a[i][2],'w'))
        connec.start()
    fw=open('metadata.txt','w')
    fw.write(filename+" "+json.dumps(a))
    return a

def nodesdictread(n=2,filename="xyz"):
    a=dict()
    # print(filename)
    filename, file_extension = filename.split(".")
    fw=open('metadata.txt','r')
    for line in fw:
        if filename in line:
            a=json.loads(line.split(" ",1)[1])
            # print(a)
    for i in a:
        connec=threading.Thread(target=w.conne,args=(a[i][0],a[i][1],a[i][2],'r'))
        connec.start()
        # time.sleep(1)
    return a

def MN_Client_establish_connection():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',55555))
    server.listen()
    print("MasterNode is listening at ",'127.0.0.1',55555)
    while True:
        client,address=server.accept()
        # print("listening")
        # print("Connected to ",str(address))
        # client.send("Connected".encode('ascii'))
        r=client.recv(1024).decode('ascii')
        # print(r)
        n,filename,op=r.split(" ")
        # filename=client.recv(1024).decode('ascii')
        # op=client.recv(1024).decode('ascii')
        n=int(n)
        op=int(op)
        # print(type(op))
        # print(op)
        if(int(op)==1):
            a=nodesdictwrite(int(n),filename)
            client.send(json.dumps(a).encode('ascii'))
        elif(int(op)==2):
            a=nodesdictread(int(n),filename)
            client.send(json.dumps(a).encode('ascii'))

        # a=nodesdictwrite(int(n),filename)
        # print(a)
        # client.send((str(a)).encode('ascii'))
        client.close()
    


import WorkerNode as w
MN_Client_establish_connection()