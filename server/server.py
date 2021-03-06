import logging
import socket

logging.basicConfig(level=logging.DEBUG)

# create a socket object
logging.info("Creating serversocket...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)


while True:
    logging.info("waiting for a client...")

    # establish a connection
    socket_to_client, addr = serversocket.accept()

    logging.info(f"Got a connection from {addr})")

    io_stream_client = socket_to_client.makefile(mode='rw')
    logging.info("waiting...")
    commando = io_stream_client.readline().rstrip('\n')
    while commando != "CLOSE":
        getal1 = io_stream_client.readline().rstrip('\n')
        logging.debug(f"Number 1: {getal1}")
        getal2 = io_stream_client.readline().rstrip('\n')
        logging.debug(f"Number 2: {getal2}")

        sum = int(getal1) + int(getal2)
        io_stream_client.write(f"{sum}\n")
        io_stream_client.flush()
        logging.debug(f"Sending back sum: {sum}")

        commando = io_stream_client.readline().rstrip('\n')

    logging.info("Connection closed...")
    socket_to_client.close()