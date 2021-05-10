import logging
import socket
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from threading import Thread
from functools import partial
import jsonpickle
import json
from models.messagehandler import MessageHandler
from queue import Queue



class WindowClient(Frame):
    def __init__(self, master=None,  user="",passwd="", socket_to_server=None, write_obj=None):
        Frame.__init__(self, master)
        self.master = master
        self.username=user
        self.password=passwd
        self.socket_to_server = socket_to_server
        self.my_writer_obj = write_obj
        print(self.socket_to_server)
        #self.makeConnnectionWithServer()
        
        self.init_window()
        #self.after(100, self.refresh)
        
    
    # Creation of init_window
    def init_window(self):
        self.master.title(f"client: {self.username}")
        

        self.server_reply = StringVar(self)
        self.server_reply.set("Placeholderdebolder")
        #self.server_reply_box = scrolledtext.ScrolledText(self, width = 20, height = 10, font = ("Times New Roman", 15), fg='black')
        self.server_reply_box = Text(self, width = 20, height = 10, font = ("Times New Roman", 15), fg='black', bg='grey')
        self.server_reply_box.grid(row=0, rowspan=6, column=2, sticky=E + W, padx=(5, 5), pady =(5,5))
        self.server_reply_box.configure(state ='disabled')
        #self.server_reply_box.pack() 

        self.artist_name = Entry(self, width=20)
        self.artist_counrty = Entry(self, width=20)
        self.artist_genre = Entry(self, width=20)

        self.artist_name.grid(row=0, column=0, sticky=E + W, padx=(5, 5), pady =(5,5))
        self.artist_counrty.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady =(5,0))
        self.artist_genre.grid(row=2, column=0, sticky=E + W, padx=(5, 5), pady =(5,0))

        Button(self,command= lambda: self.sendmessage("Q0", self.artist_name.get()),text="Search artist info by name",width=30).grid(row=0,column=1,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q1", self.artist_counrty.get()),text="Search artist by country",width=30).grid(row=1,column=1,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q2", self.artist_genre.get()),text="Search top artists by genre",width=30).grid(row=2,column=1,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q3", "SOMETHING"),text="Give a histogram of most popular genres",width=60).grid(row=4,column=0,columnspan = 2,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.sendmessage("Q4", "SOMETHING"),text="And another query",width=10).grid(row=5,column=0,columnspan = 2,sticky=E+W,padx=(5, 5), pady =(5,5))
        Button(self,command= lambda: self.close_connection,text="close connection",width=20).grid(row=6,column=0,sticky=E+S+W,pady=(20,0),padx=(10,0))

        Grid.rowconfigure(self, 7, weight=1)
        Grid.columnconfigure(self, 3, weight=1)

        self.pack(fill=BOTH, expand=1)

        #self.recieve_messages()

        self.queue = Queue()

       

        #receiver_thread = Thread(name='receiver_thread', target= lambda: self.recieve_messages)
        #receiver_thread.setDaemon(True)
        #receiver_thread.start()

        self.monitor()
        
        
        #receiver_thread = MessageHandler("Message-handler", self.server_reply_box, self, self.my_writer_obj)
        #receiver_thread.start()

        #self.monitor(receiver_thread)

        
    
    def __del__(self):
        self.close_connection()

    def makeConnnectionWithServer(self):
        try:
            #logging.info("Making connection with server...")
            # get local machine name
            #self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #host = socket.gethostname()
            #port = 9999
            # connection to hostname on the port.
            #self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode='rw')
            #logging.info("Open connection with server succesfully")

            receiver_thread = MessageHandler("Message-handler", self.server_reply_box, self, self.my_writer_obj)
            receiver_thread.run()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.my_writer_obj.write("CLOSE\n")
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            print("testerror")
        
        self.master.destroy()
    
    def sendmessage(self, query_number, query_param):
        try:
            self.server_reply.set("")
            logging.info(f"Sending {query_number} with param {query_param}")
            self.my_writer_obj.write(f"{self.username};{query_number};{query_param}\n")
            self.my_writer_obj.flush()
            

            answer = self.my_writer_obj.readline().rstrip('\n')
            answer = answer.split(';')
            pickle_data = jsonpickle.decode(answer[1])
            clean_data = json.loads(pickle_data)
            
            self.write_to_list(clean_data, "TODO")
            #print(type(pickle_data))

        except Exception as ex:
            print(ex)

    def create_client(username, passwd, socket_server, write_obj):
        root = Tk()
        root.geometry("800x300")
        app = WindowClient(root, username, passwd, socket_server, write_obj)
        root.mainloop()

    def recieve_messages(self):
        logging.debug("THREAD IS ALIVE")
        #mogelijkheid voor Queue tussen te plaatsen
        message = self.my_writer_obj.readline().rstrip('\n').split(';')
        logging.debug(message)
        while message[0] != 'CLOSE':
            logging.debug(message)
            if len(message) > 0:
                logging.info(f"Answer server: {message}")

            if message[0] == 'moderator':
                logging.info(f"Moderator: {message}")

            elif message[0] == 'text_response':
                pickle_data = jsonpickle.decode(message[1])
                clean_data = json.loads(pickle_data)
                #self.write_to_list(clean_data, "TODO")
                self.queue.put(clean_data)
                logging.info(f"Answer server: {clean_data}")

            message = self.my_writer_obj.readline().rstrip('\n').split(';')

        #self.after(100, lambda: self.recieve_messages)
    
    def write_to_list(self, data, header):
        self.server_reply_box.configure(state ='normal')
        self.server_reply_box.delete('1.0', END)
        for index, text in enumerate(data):
            self.server_reply_box.insert(INSERT, f'{index+1}. {text}\n')
        self.server_reply_box.configure(state ='disabled')

    def monitor(self):
        if self.queue.empty():
            pass
        else:
            message = self.queue.get_nowait()
            self.write_to_list(message, "TODO")
        
        self.after(100, self.monitor)

    # def monitor(self, thread):
    #     if thread.is_alive():
    #         # check the thread every 100ms
            

    #         if len(thread.message) > 0:
    #             logging.info(f"Answer server: {thread.message}")

    #         if thread.message[0] == 'moderator':
    #             logging.info(f"Moderator: {thread.message}")

    #         elif thread.message[0] == 'text_response':
  
    #             self.write_to_list(thread.clean_data, "TODO")
    #             logging.info(f"Answer server: {thread.clean_data}")


# root = Tk()
# # root.geometry("400x300")
# app = Window(root)
# root.mainloop()

if __name__ == '__main__':
    client = WindowClient.create_client("test", "tester")
    client = mainloop()