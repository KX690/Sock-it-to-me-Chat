import socket
import threading

username = input("Introduzca su nombre: ")

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((host, port))
    print("Connected to the server")
except Exception as e:
    print(f"Unable to connect: {e}")

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except Exception as e:
            print(f"Error receiving messages: {e}")
            client.close()
            break

def write_messages():
    while True:
        message = f"{username}: {input('')}"
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending messages: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()