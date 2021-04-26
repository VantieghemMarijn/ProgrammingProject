import socket
import sys

print("Making connection with server...")
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# connection to hostname on the port.
s.connect((host, port))
io_stream_server = s.makefile(mode='rw')

vraag = "Geef opdracht door:\n 's' om som van 2 getallen te berekenen,\n 'c' om af te sluiten>:"
actie = input(vraag)
while (actie != 'c'):
    io_stream_server.write("CALCLULATE_SUM\n")
    io_stream_server.flush()

    # ask 2 numbers
    number1 = input("Eerste getal: ")
    number2 = input("Tweede getal: ")

    io_stream_server.write(f"{number1}\n")
    io_stream_server.write(f"{number2}\n")
    io_stream_server.flush()

    print("Waiting for answer...")
    sum = io_stream_server.readline().rstrip('\n')
    print(f"Sum of the 2 numbers: {sum}")
    actie = input(vraag)

io_stream_server.write("CLOSE\n")
io_stream_server.flush()
print("Close connection with server...")
s.close()
