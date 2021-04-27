import socket
import sys
import login_gui

print("Making connection with server...")
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999
stop=False
# connection to hostname on the port.
s.connect((host, port))
io_stream_server = s.makefile(mode='rw')




def getmessage():
    
    print("moderator message")
    message = io_stream_server.readline().rstrip('\n')
    print(message)
    io_stream_server.flush()    

while (stop==False):
    
    
    

io_stream_server.write("CLOSE\n")
io_stream_server.flush()
print("Close connection with server...")
s.close()
