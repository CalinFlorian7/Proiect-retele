from src.server.product.Product import Product
from src.server.user.User import User
from src.server.auction.Bid import Bid
from time import struct_time, localtime
from uuid import uuid4


class Auction:

    __id: str
    __owner: str
    __product: Product
    __bids: list[Bid]
    __started_at: struct_time

    def __init__(self, username: str, product: Product):
        self.__id = uuid4()
        self.__product = product
        self.__owner = username
        self.__bids = []
        self.__started_at = localtime()

    def get_owner(self):
        return self.__owner

    def get_product(self):
        return self.__product

    def get_last_bid(self):
        if len(self.__bids) == 0:
            return None
        return self.__bids[-1]

    def get_started_at(self):
        return self.__started_at

    def return_current_price(self):
        return "and current price: " + \
            str(self.get_last_bid().get_price()
                ) if self.get_last_bid() is not None else ""

    def __str__(self):
        return f"Product {self.__product.get_name()} owned by {self.get_owner()} with starting price {self.__product.get_starting_price()} {self.return_current_price()}"

    def bid(self, bid_amount, user: User):
        self.__bids.append(Bid(bid_amount, user.get_name()))

    def is_user_participating(self, user: User):
        for bid in self.__bids:
            if bid.get_bidder() == user.get_name():
                return True
        return False
