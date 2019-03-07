from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
BUFSIZ = 1024

def accept_incoming_connections(SERVER):
    print("Setting up a server")
    while True:
        print("waiting for client to join....")
        client, client_address = SERVER.accept()
        addresses[client] = client_address
        print("%s:%s has connected." % client_address)
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.    
    client.send(bytes("Greetings from the cave!\nEnter your name in the message window below", "utf8"))

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            del clients[client]
            client.close()
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.    
    for user in clients:
        user.send(bytes(prefix, "utf8")+msg)
