import logging
import socket
from tkinter import *
from tkinter import messagebox
from client_gui import WindowClient


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        # self.makeConnnectionWithServer()
      
        
    # Creation of init_window
    def init_window(self):

        self.master.title("login_screen")
        self.pack(fill=BOTH, expand=1)

        Label(self, text="username:").grid(row=0)
        self.entry_username = Entry(self, width=40)
        self.entry_username.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady =(5,5))

        Label(self, text="passsword:", pady=10).grid(row=2)
        self.entry_passsword = Entry(self, width=40)
        self.entry_passsword.grid(row=3, column=0, sticky=E + W, padx=(10, 10), pady =(5,0))

        Button(self,command=self.login,text="test",width=10).grid(row=4,column=0,sticky=S,pady=(20,0))
        

        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    
    

    def __del__(self):
        self.close_connection()

    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def login(self):
        logging.info("loggin in")
        username=self.entry_username.get()
        passwd=self.entry_passsword.get()
        logging.info(f"{username},{passwd}")
        self.master.destroy()
        WindowClient.create_client(username,passwd)  

logging.basicConfig(level=logging.INFO)

root = Tk()
# root.geometry("400x300")
app = Window(root)
root.mainloop()
