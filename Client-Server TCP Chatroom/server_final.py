import socket
import threading
import tkinter as tk

class ServerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP ServerUI")

        self.host_label = tk.Label(root, text="Host: localhost")
        self.host_label.pack()

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_server)
        self.start_button.pack()

        self.message_label = tk.Label(root, text="Server Message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(root)
        self.message_entry.pack()

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.message_history = tk.Text(root)
        self.message_history.pack()

        self.server = None
        self.clients = {}
        self.nicknames = {}

    def start_server(self):
        if self.server:
            self.message_history.insert(tk.END, "Server already running.\n")
            return

        port = int(self.port_entry.get())

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', port))
        self.server.listen()
        self.start_button.config(state=tk.DISABLED)

        self.message_history.insert(tk.END, f"Server running on port {port}...\n")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        
        if message:
            self.message_history.insert(tk.END, f"Server: {message}\n")
            self.broadcast(f"Server: {message}".encode('ascii'))

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message.decode('ascii').startswith('@'):
                    recipient = message.decode('ascii').split()[0][1:]
                    message = message[len(recipient) + 2:]
                    self.clients[self.nicknames[recipient]].send(f"{self.nicknames[client]}: {message}".encode('ascii'))
                else:
                    self.broadcast(f"{self.nicknames[client]}: {message}".encode('ascii'))
            except:
                index = self.clients.index(client)
                self.clients.pop(client)
                client.close()
                nickname = self.nicknames[client]
                self.broadcast(f"{nickname} left the chat!".encode('ascii'))
                self.nicknames.pop(client)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            self.message_history.insert(tk.END, f"Connected with {str(address)}\n")

            #client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames[client] = nickname
            self.clients[client] = None

            self.message_history.insert(tk.END, f"Nickname of the client is {nickname}\n")
            self.broadcast(f"{nickname} joined the chat!".encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

root = tk.Tk()
app = ServerUI(root)
root.mainloop()
