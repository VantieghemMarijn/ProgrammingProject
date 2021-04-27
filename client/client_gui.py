import logging
import socket
from tkinter import *
from tkinter import messagebox


class WindowClient(Frame):
    def __init__(self, master=None,user="",passwd=""):
        Frame.__init__(self, master)
        self.master = master
        self.username=user
        self.password=passwd
        self.init_window()
        self.makeConnnectionWithServer()
        

    
    # Creation of init_window
    def init_window(self):
        self.master.title(f"client: {self.username}")
        self.pack(fill=BOTH, expand=1)

        Button(self,command=self.sendmessage("1"),text="search artist on name",width=30).grid(row=0,column=0,sticky=E+W,pady=(20,0),padx=(10,0))
        Button(self,command=self.sendmessage("2"),text="search artist by country",width=30).grid(row=1,column=0,sticky=E+W,pady=(20,0),padx=(10,0))
        Button(self,command=self.sendmessage("3"),text="search all artists by genre",width=10).grid(row=2,column=0,sticky=E+W,pady=(20,0),padx=(10,0))
        Button(self,command=self.close_connection,text="close connection",width=20).grid(row=3,column=0,sticky=E+S+W,pady=(20,0),padx=(10,0))

        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def __del__(self):
        self.close_connection()

    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname()
            port = 9999
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode='rw')
            logging.info("Open connection with server succesfully")
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
    
    def sendmessage(self,query):
        try:
            logging.info("Sending message")
            if(query=="1"):
                self.my_writer_obj.write(f"user:{self.username} message:1\n")
                
            elif(query=="2"):
                self.my_writer_obj.write(f"user:{self.username} message:2\n")
                
            elif(query=="3"):
                self.my_writer_obj.write(f"user:{self.username} message:3\n")
            self.my_writer_obj.flush()
        except Exception as ex:
            print(ex)

    def create_client(usernmame,passwd):
        root = Tk()
        root.geometry("400x300")
        app = WindowClient(root,usernmame,passwd)
        root.mainloop()



#WindowClient.create_client()