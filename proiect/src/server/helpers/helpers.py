from socket import socket
from src.server.user.UserRegistry import UserRegistry
from src.server.product.Product import Product
from src.server.auction.Auction import Auction
from threading import Lock

from src.server.utils.utils import do_with_lock

def is_product_auctioned(product: Product, auctions: list[Auction]):
    for auction in auctions:
        if auction.get_product() == product:
            return True
    return False

def send_message_to_client(message: str, client_socket: socket):
    try:
        if client_socket is not None:
            client_socket.send(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")


def get_client_response(client_socket: socket):
    try:
        response = client_socket.recv(1024).decode()
        return response
    except Exception as e:
        print(f"Error receiving response from client: {e}")
        return None


def broadcast_to_all_clients(message: str, sender_socket: socket,  users: dict):
    for user in users.values():
        user_socket = user.get_client_socket();
        if user_socket != sender_socket and user_socket is not None:
            user_socket.send(message.encode())


def broadcast(message: str, sender_socket: socket, users: UserRegistry, lock: Lock):
    do_with_lock(lock, broadcast_to_all_clients, message, sender_socket, users)
