import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.bind((host, port)) 
server.listen()
print(f"El servidor se esta ejecutando {host}:{port}")

clients = [] 
usernames = [] 

def broadcast(message, _client): 
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024) 
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"{username} Desconectado".encode('utf-8')) 
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} esta conectado con {str(address)}")

        message = f"{username} Se conecto al chat!".encode('utf-8')
        broadcast(message, client)
        client.send("Conectado al servidor".encode('utf-8'))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()

          