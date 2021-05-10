import logging
import threading
from .ArtistRepository import ArtistRepository
import jsonpickle


import pickle

class ClientHandler(threading.Thread):

    def __init__(self, socketclient, server_message_queue):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient
        self.ArtistRepository = ArtistRepository()
        self.server_message_queue = server_message_queue

    def run(self):
        io_stream_client = self.socket_to_client.makefile(mode='rw')
        logging.info("CLH - started & waiting...")
        commando = io_stream_client.readline().rstrip('\n')
        while commando != "CLOSE":
            logging.info(commando)
            logging.info("CLH - Something came in")

            

            message = commando.split(';')
            logging.info(message)

            username = message[0]
            query_number = message[1]
            query_param = message[2]

            self.server_message_queue.put(f"New request from user {username} for query {query_number} with param {query_param}")

            logging.debug(f"CLH - Username: {username}")
            logging.debug(f"CLH - Query number: {query_number}")
            logging.debug(f"CLH - Query param: {query_param}")

 

            data = self.ArtistRepository.execute_query(query_number, query_param)

            json_pickle = jsonpickle.encode(data)
            logging.debug(json_pickle)
            

            io_stream_client.write(f"text_response;{json_pickle}\n")
            io_stream_client.flush()

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
