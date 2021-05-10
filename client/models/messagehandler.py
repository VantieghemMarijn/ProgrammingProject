import threading
import logging
import jsonpickle
import json

class MessageHandler(threading.Thread):
    
    def __init__(self, name="Message-handler", server_reply_box=None, root_app=None, my_writer_obj=None):
        super().__init__(name=name)
        self.daemon = True
        self.server_reply_box = server_reply_box
        self.root_app = root_app
        self.my_writer_obj = my_writer_obj

        self.message = ""
        self.clean_data = None

        logging.info(f"Thread is alive")

    def run(self):
        # run forever
        self.message = self.my_writer_obj.readline().rstrip('\n').split(';')
        while self.message != "CLOSE":
            pickle_data = jsonpickle.decode(self.message[1])
            self.clean_data = json.loads(pickle_data)
            self.message = self.my_writer_obj.readline().rstrip('\n').split(';')
