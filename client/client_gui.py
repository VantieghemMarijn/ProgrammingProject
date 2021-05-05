import logging
import socket
from tkinter import *
from tkinter import messagebox
from threading import Thread
from functools import partial


genres = [

]



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
        
    
    # Creation of init_window
    def init_window(self):
        self.master.title(f"client: {self.username}")
        self.pack(fill=BOTH, expand=1)

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
        Grid.columnconfigure(self, 1, weight=1)

        #t = Thread(target=self.recieve_messages, name="messages-queue")
       #t.start()

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
            logging.info(f"Sending {query_number} with param {query_param}")
            self.my_writer_obj.write(f"{self.username} {query_number} {query_param}\n")
            
            # if(query=="1"):
            #     logging.info("KWERIE")
            #     self.my_writer_obj.write(f"user:{self.username} message:1\n")
                
            # elif(query=="2"):
            #     self.my_writer_obj.write(f"user:{self.username} message:2\n")
                
            # elif(query=="3"):
            #     self.my_writer_obj.write(f"user:{self.username} message:3\n")
            self.my_writer_obj.flush()
        except Exception as ex:
            print(ex)

    def create_client(usernmame, passwd, socket_server, write_obj):
        root = Tk()
        root.geometry("400x300")
        app = WindowClient(root, usernmame, passwd, socket_server, write_obj)
        root.mainloop()

    def recieve_messages(self):
        #mogelijkheid voor Queue tussen te plaatsen
        logging.info(f"moderator: {message}")
# root = Tk()
# # root.geometry("400x300")
# app = Window(root)
# root.mainloop()

# if __name__ == '__main__':
#     client = WindowClient.create_client("test", "tester")
#     client = mainloop()