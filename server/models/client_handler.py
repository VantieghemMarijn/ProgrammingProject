import logging
import threading


class ClientHandler(threading.Thread):

    def __init__(self, socketclient):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient

    def run(self):
        io_stream_client = self.socket_to_client.makefile(mode='rw')
        logging.info("CLH - started & waiting...")
        commando = io_stream_client.readline().rstrip('\n')
        while commando != "CLOSE":
            logging.info("CLH - Something came in")
            message = io_stream_client.readline().rstrip('\n').split(' ')

            username = message[0]
            query_number = message[1]
            query_param = message[2]

            logging.debug(f"CLH - Username: {username}")
            logging.debug(f"CLH - Query number: {query_number}")
            logging.debug(f"CLH - Query param: {query_param}")

            # getal1 = io_stream_client.readline().rstrip('\n')
            # logging.debug(f"CLH - Number 1: {getal1}")
            # getal2 = io_stream_client.readline().rstrip('\n')
            # logging.debug(f"CLH - Number 2: {getal2}")

            # sum = int(getal1) + int(getal2)
            # io_stream_client.write(f"{sum}\n")
            # io_stream_client.flush()
            # logging.debug(f"CLH - Sending back sum: {sum}")

            commando = io_stream_client.readline().rstrip('\n')

        logging.debug(f"CLH - Connection closed...")
        self.socket_to_client.close()
