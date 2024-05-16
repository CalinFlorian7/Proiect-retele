import socket
import json
import threading
import time

from src.server.user.UserRegistry import UserRegistry
from src.server.user.User import User
from src.server.product.Product import Product
from src.server.product.ProductRegistry import ProductRegistry
from src.server.auction.Auction import Auction

from src.server.helpers.helpers import send_message_to_client, get_client_response, broadcast_to_all_clients, is_product_auctioned
from src.server.utils.utils import tryParseFloat


class Server:

    __host: str
    __port: int
    __server_socket: socket
    __lock: threading.Lock
    __users: UserRegistry
    __products: ProductRegistry
    __auctions: list[Auction]

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__lock = threading.Lock()
        self.__users = UserRegistry()
        self.__products = ProductRegistry()
        self.__auctions = []

    def start(self):
        try:
            self.__server_socket.bind((self.__host, self.__port))
            self.__server_socket.listen(5)
            print(f"Server started on {self.__host}:{self.__port}")

            while True:
                try:
                    client_socket, client_address = self.__server_socket.accept()
                    print(
                        f"New connection from {client_address[0]}:{client_address[1]}")

                    client_thread = threading.Thread(
                        target=self.handle_client, args=(client_socket,))
                    client_thread.start()

                except Exception as e:
                    print(str(e))
                    self.stop()

        except Exception as e:
            print(str(e))
            self.stop()

    def stop(self):
        with self.__lock:
            for client_socket in self.__users.get_users().values():
                client_socket.close()
        self.__server_socket.close()

    def handle_client(self, client_socket):
        try:
            user = self.insert_user(client_socket)
        except Exception as e:
            print(str(e))
            self.__server_socket.close()
        try:
            self.list_available_products(
                client_socket, send_message_to_client)
            while True:
                send_message_to_client(
                    "Please select an option:\n1. Add a product\n2. Auction an item\n3. Bid on item\n4. See your products \n5. See auctioned products", client_socket)
                option = get_client_response(client_socket)
                if option == "1":
                    self.insert_product(client_socket, user)
                elif option == "2":
                    self.auction_item(client_socket, user)
                elif option == "3":
                    self.bid_on_item(client_socket, user)
                elif option == "4":
                    self.list_your_products(client_socket, user)
                elif option == "5":
                    self.list_available_products(
                        client_socket, send_message_to_client)
                else:
                    send_message_to_client(
                        "Please select an available option!\n", client_socket)

        except Exception:
            self.__users.remove_user(user)
            self.__products.remove_user_products(user)
            client_socket.close()

    def insert_user(self, client_socket):
        send_message_to_client(
            "To enter the auction, please enter your username: ", client_socket)
        while True:
            username = get_client_response(client_socket)
            if username == "":
                send_message_to_client(
                    "Please enter a valid username!", client_socket)
            elif self.__users.username_exists(username):
                send_message_to_client(
                    "The username already exists, please enter another username: ", client_socket)
            else:
                user = User(username, client_socket)
                self.__users.add_user(user)
                return user

    def insert_product(self, client_socket: socket, user: User):
        try:
            while True:
                send_message_to_client(
                    "Please enter the product name: ", client_socket)
                product_name = get_client_response(client_socket)
                send_message_to_client(
                    "Please enter the starting price: ", client_socket)
                starting_price = get_client_response(client_socket)
                if product_name == "":
                    send_message_to_client(
                        "Please enter a valid product name!", client_socket)
                elif starting_price == "" or not tryParseFloat(starting_price):
                    send_message_to_client(
                        "Please enter a valid starting price!", client_socket)
                else:
                    product = Product(product_name, float(starting_price))
                    self.__products.add_product(user, product)
                    send_message_to_client(
                        "The product was added", client_socket)
                    return

        except Exception as e:
            print(str(e))

    def auction_item(self, client_socket: socket, user: User):
        try:
            products = self.list_your_available_products(client_socket, user)
            if products is None:
                send_message_to_client(
                    "You have no products available!", client_socket)
                return
            while True:
                send_message_to_client(
                    "Please write a product index to start the auction: ", client_socket)
                product_index = get_client_response(client_socket)
                while True:
                    if product_index == "":
                        send_message_to_client(
                            "Please enter a valid index!", client_socket)
                    elif not product_index.isdigit():
                        send_message_to_client(
                            "Please enter a valid index!", client_socket)
                    elif int(product_index) >= len(products):
                        send_message_to_client(
                            "The product does not exist, please enter a valid index!", client_socket)
                    elif int(product_index) < 0:
                        send_message_to_client(
                            "The product does not exist, please enter a valid index!", client_socket)
                    else:
                        auction = Auction(
                            user.get_name(), products[int(product_index)])
                        self.__auctions.append(auction)
                        broadcast_to_all_clients(f"An auction has started by {user.get_name()} for the product: \n" + str(auction), client_socket, self.__users.get_users())
                        threading.Thread(target=self.handle_auction, args=(
                            client_socket, auction)).start()
                        return
        except ConnectionResetError as e:
            print(str(e))

    def handle_auction(self, client_socket: socket, auction: Auction):
        once = False
        while True:
            if time.time() - time.mktime(auction.get_started_at()) > 60:
                broadcast_to_all_clients(
                    f"The auction for {str(auction)} has ended!", client_socket, self.__users.get_users())
                send_message_to_client(
                    f"Your auction for {str(auction)} has ended!", client_socket)
                if auction.get_last_bid() is not None:
                    broadcast_to_all_clients(f"Winner: {auction.get_last_bid().get_bidder()} with the price of {auction.get_last_bid().get_price()}", None, self.__users.get_users())
                product = auction.get_product()
                if auction.get_last_bid() is not None:
                    product.set_was_sold(True)
                    product.set_max_bid(auction.get_last_bid())
                else:
                    auction.get_product().set_was_sold(False)
                self.__auctions.remove(auction)
                return

            if time.time() - time.mktime(auction.get_started_at()) > 30 and not once:
                send_message_to_client(
                    f"The auction for {str(auction)} will end in ~30 seconds!", client_socket)
                broadcast_to_all_clients(
                    f"The auction for {str(auction)} will end in ~30 seconds!", client_socket, self.__users.get_users())
                once = True

    def bid_on_item(self, client_socket: socket, user: User):
        send_message_to_client(
            "Please wait for current bids to be done!", client_socket)
        with self.__lock:
            try:
                products = self.list_available_products(
                    client_socket, send_message_to_client)
                if products is None:
                    send_message_to_client(
                        "You have no products available!", client_socket)
                    return
                while True:
                    send_message_to_client(
                        "Please write a product index to bid on: ", client_socket)
                    while True:
                        product_index = get_client_response(client_socket)
                        if product_index == "":
                            send_message_to_client(
                                "Please enter a valid index!", client_socket)
                        elif not product_index.isdigit():
                            send_message_to_client(
                                "Please enter a valid index!", client_socket)
                        elif int(product_index) >= len(self.__auctions):
                            send_message_to_client(
                                "The product does not exist, please enter a valid index!", client_socket)
                        elif int(product_index) < 0:
                            send_message_to_client(
                                "The product does not exist, please enter a valid index!", client_socket)
                        else:
                            auction = self.__auctions[int(product_index)]
                            send_message_to_client(
                                "Please enter the amount you want to bid: ", client_socket)
                            bid_amount = get_client_response(client_socket)
                            if not tryParseFloat(bid_amount):
                                send_message_to_client(
                                    "Please enter a valid amount!", client_socket)
                            elif float(bid_amount) <= auction.get_product().get_starting_price():
                                send_message_to_client(
                                    "The bid amount must be higher than the current price!", client_socket)
                            elif auction.get_last_bid() is not None and float(bid_amount) <= auction.get_last_bid().get_price():
                                send_message_to_client(
                                    "The bid amount must be higher than the current price!", client_socket)
                            else:
                                auction.bid(float(bid_amount),
                                            user)
                                # filter users that are not the sender if they are in the bid list
                                cc = {k: v for k, v in self.__users.get_users(
                                ).items() if auction.is_user_participating(v) or v.get_name() == auction.get_owner()}
                                broadcast_to_all_clients(
                                    f"{user.get_name()} has bid {bid_amount} on {str(auction)}", client_socket, cc)
                                return
            except Exception as e:
                print(str(e))

    def list_your_products(self, client_socket, user):
        try:
            products = self.__products.get_user_products(user)
            if (len(products) == 0 or products is None):
                send_message_to_client(
                    "You have no products available!", client_socket)
                return None
            send_message_to_client(
                "The products you have added are:", client_socket)
            index = 0
            for product in products:
                send_message_to_client(str(index) + ". " +
                                       str(product) + "\n", client_socket)
                index += 1
            return products
        except Exception as e:
            print(str(e))

    def list_your_available_products(self, client_socket: socket, user):
        try:
            products = self.__products.get_user_products(user)
            products = [
                product for product in products if not product.get_was_sold()]
            products = [product for product in products if not is_product_auctioned(
                product, self.__auctions)]
            if (len(products) == 0 or products is None):
                send_message_to_client(
                    "You have no products available!", client_socket)
                return None
            send_message_to_client(
                "The products you have added are:", client_socket)
            index = 0
            for product in products:
                send_message_to_client(str(index) + ". " +
                                       str(product) + "\n", client_socket)
                index += 1
            return products
        except Exception as e:
            print(str(e))

    def list_available_products(self, client_socket: socket, send, users=None):
        try:
            auctions = self.__auctions
            if (len(auctions) == 0 or auctions is None):
                if users is None:
                    send(
                        "No auctioned products available!", client_socket)
                else:
                    send(
                        "No auctioned products available!", client_socket, users)
                return None
            else:
                if users is None:
                    send(
                        "The auctioned products are:", client_socket)
                else:
                    send(
                        "The auctioned products are:", client_socket, users)
                index = 0
                for auction in auctions:
                    if users is None:
                        send(str(index) + ". " +
                             str(auction) + "\n", client_socket)
                    else:
                        send(str(index) + ". " +
                             str(auction) + "\n", client_socket, users)
                    index += 1
                return auctions
        except Exception as e:
            print(str(e))
