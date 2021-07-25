import socket
import threading

PORT=50004
HOST=socket.gethostbyname(socket.gethostname())

ADDRESS=(HOST,PORT)

FORMAT='utf-8'

clients=[]
names=[]

#create a new socket for server connection where AF_INET is the type of address
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)

def startchat():
  print("Server is working on "+HOST)
  
  server.listen()

  while True:
    connection, addr = server.accept()
    connection.send("NAME".encode(FORMAT))

    name = connection.recv(2050).decode(FORMAT)
    names.append(name)
    clients.append(connection)

    print(f"name is:{name}")

    broadcastMessage(f"{name} has joined the group".encode(FORMAT))

    connection.send("Connection successful".encode(FORMAT))

    thread = threading.Thread(target=receive, args=(connection,addr))

    thread.start()

    print(f"active connections {threading.active_count()-1}")

def receive(connection,addr):
    print(f"New Connection {addr}")

    connected = True

    while connected:
        message = connection.recv(2050)

        broadcastMessage(message)
    connection.close()

def broadcastMessage(message):
  for client in clients:
      client.send(message)


startchat()

#this code is completed by Durgesh Kumar
