import socket
import threading
from tkinter import *

def get_port():
  """
  Gets the port number entered by the user and sets the 'PORT' variable.
  """
  global PORT
  PORT = int(entry_port.get())
  window.destroy()  # Close the window after getting the port

# Create the main window for port selection
window = Tk()
window.title("Enter Port")

# Create a label
label_port = Label(window, text="Port:")
label_port.pack()

# Create an entry field for user input
entry_port = Entry(window)
entry_port.pack()

# Create a submit button
button_submit = Button(window, text="Submit", command=get_port)
button_submit.pack()

# Initialize the port variable (optional)
PORT = None

# Start the GUI event loop for port selection
window.mainloop() 

# Now the port is set and the mainloop has finished

# An IPv4 address is obtained
# for the server.
SERVER = socket.gethostbyname(socket.gethostname())

# Address is stored as a tuple
ADDRESS = (SERVER, PORT)

# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"

# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []

# Create a new socket for
# the server
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

# bind the address of the
# server to the socket
server.bind(ADDRESS)

# function to start the connection


def startChat():

    print("server is working on " + SERVER)

    # listening for connections
    server.listen()

    while True:

        # accept connections and returns
        # a new connection to the client
        # and the address bound to it
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))

        # 1024 represents the max amount
        # of data that can be received (bytes)
        name = conn.recv(1024).decode(FORMAT)

        # append the name and client
        # to the respective list
        names.append(name)
        clients.append(conn)

        print(f"Name is :{name}")

        # broadcast message
        broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))

        conn.send('Connection successful!'.encode(FORMAT))

        # Start the handling thread
        thread = threading.Thread(target=handle,
                                   args=(conn, addr))
        thread.start()

        # no. of clients connected
        # to the server
        print(f"active connections {threading.activeCount()-1}")

# method to handle the
# incoming messages


def handle(conn, addr):

    print(f"new connection {addr}")
    connected = True

    while connected:
        # receive message
        message = conn.recv(1024)

        # broadcast message
        broadcastMessage(message)

    # close the connection
    conn.close()

# method for broadcasting
# messages to the each clients


def broadcastMessage(message):
    for client in clients:
        client.send(message)


# call the method to
# begin the communication
startChat()