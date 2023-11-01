import threading
import socket
from datetime import datetime,date

class Servidor:
    def __init__(self, host = socket.gethostname(), port = 55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.names = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == '/sair':
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    name = self.names[index]
                    self.names.remove(name)
                    self.broadcast(f'{name} foi desconectado!'.encode('utf-8'))
                    break
                print(f'{message}')
                with open('log.txt', 'a') as f:
                    f.write(f'{message}\n')
                timestamped_message = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {message}'.encode('utf-8')
                self.broadcast(message.encode('utf-8'))
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                name = self.names[index]
                self.names.remove(name)
                self.broadcast(f'{name} foi desconectado!'.encode('utf-8'))
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'CONNECTED -> {str(address)}')
            client.send('NICK'.encode('utf-8'))
            name = client.recv(1024).decode('utf-8')
            self.names.append(name)
            self.clients.append(client)
            print(f'nome do cliente é {name}!')
            self.broadcast(f'{name} entrou!'.encode('utf-8'))
            client.send('Conectado ao servidor!'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,)) 
            thread.start()  

if __name__ == "__main__":
    with open('log.txt', 'a') as f:
        f.write(f'Chat iniciado em {date.today()}\n\n')
    print('Chat iniciado !')
    servidor = Servidor()  
    servidor.receive()  
