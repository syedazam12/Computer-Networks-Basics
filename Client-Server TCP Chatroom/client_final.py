import socket
import threading
import tkinter as tk

class ClientUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP ClientUI")

        self.host_label = tk.Label(root, text="Host:")
        self.host_label.pack()

        self.host_entry = tk.Entry(root)
        self.host_entry.pack()

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.nickname_label = tk.Label(root, text="Nickname:")
        self.nickname_label.pack()

        self.nickname_entry = tk.Entry(root)
        self.nickname_entry.pack()

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_server)
        self.connect_button.pack()

        self.message_label = tk.Label(root, text="Client Message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(root)
        self.message_entry.pack()

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.message_history = tk.Text(root)
        self.message_history.pack()

        self.client_socket = None
        self.nickname = None

    def connect_server(self):
        if self.client_socket:
            self.message_history.insert(tk.END, "Already connected to a server.\n")
            return

        host = self.host_entry.get()
        port = int(self.port_entry.get())
        self.nickname = self.nickname_entry.get()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.client_socket.send(f"{self.nickname} has joined the chat.".encode('ascii'))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message.strip() == "":
            return
        self.message_entry.delete(0, tk.END)
        self.message_history.insert(tk.END, f"{self.nickname}: {message}\n")
        self.client_socket.send(f"{self.nickname}: {message}".encode('ascii'))

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('ascii')
                self.message_history.insert(tk.END, f"{message}\n")
            except:
                self.message_history.insert(tk.END, "Connection closed by server.\n")
                self.client_socket.close()
                break

root = tk.Tk()
app = ClientUI(root)
root.mainloop()