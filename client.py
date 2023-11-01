import socket 
import threading
from datetime import datetime

server_host = input("rede: ")
name = input("Escolha um nome: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_host, 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print("Conexão encerrada!")
            break

def write():
    while True:
        message = f'{input("")}'
        if message.lower() == '/sair':
            client.send(message.encode('utf-8'))
            client.close()
            break
        client.send(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n{name} diz: {message}'.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
