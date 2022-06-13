import socket
import threading

HOST = '127.0.0.1' #localhost, si on veut heberger l'appli en ligne il faudrait récupérer l'@IP en utilisant ipconfig sur CMD
PORT = 9090


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.SOCK_STREAM est le traitement TCP
server.bind((HOST, PORT))

server.listen()

clients = [] #list vide de client
nicknames = []#pour mieux gérer les clientsbroadcast


#diffusion
def broadcast(message):
    for client in clients:
        client.send(message)

#manipuler

def handle(client):
    while True: #on essaie ici d'envoyer le code si ça ne marche pas on renvoie une exception d'erreur qu'on peut gérer
        try:
            message = client.recv(1024)#si le client reçoit les 1024 bits on passe à la diffusion
            print(f"{nicknames[clients.index(client)]} dit {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

#recevoir, c'est aussi la fonction qui accepte les connexions
def receive():
    while True:
        client, address = server.accept()
        print(f"{str(address)} est connecté!")

        client.send("NICK".encode('utf-8'))#pour envoyer l'alias (nickname)
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Alias du client est {nickname}")
        broadcast(f"{nickname} est connecté au server!\n".encode('utf-8'))
        client.send("vous êtes connecté au server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()




print("Server runing****")

receive()