import logging
import socket
# create a socket object
import threading

from models.client_handler import ClientHandler


logging.basicConfig(level=logging.DEBUG)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)


while True:
    logging.info("Server: waiting for a client...")

    # establish a connection
    socket_to_client, addr = serversocket.accept()

    logging.info(f"Server: Got a connection from {addr})")
    clh = ClientHandler(socket_to_client)
    clh.run()
    logging.info(f"Server: ok, clienthandler started. Current Thread count: {threading.active_count()}.")