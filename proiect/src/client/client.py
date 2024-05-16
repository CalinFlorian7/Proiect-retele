import socket
import threading


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiveDataThread = threading.Thread(target=self.receive_data)
        self.sendDataThread = threading.Thread(target=self.send_data)

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.receiveDataThread.start()
            self.sendDataThread.start()
        except ConnectionRefusedError:
            print("Failed to connect to the server.")
            exit(1)

    def send_data(self):
        try:
            while True:
                data = input()
                self.client_socket.sendall(data.encode())
        except socket.error as e:
            print("Failed to send data:", str(e))

    def receive_data(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                self.print_message(data)
        except socket.error as e:
            print("Failed to receive data:", str(e))

    def print_message(self, message):
        print(message)

    def close(self):
        self.client_socket.close()
