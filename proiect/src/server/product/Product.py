from src.server.auction.Bid import Bid


class Product:
    __name: str
    __starting_price: float
    __max_bid: Bid
    __was_sold: bool

    def __init__(self, name, starting_price):
        self.__name = name
        self.__starting_price = starting_price
        self.__was_sold = False
        self.__max_bid = None

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_starting_price(self):
        return self.__starting_price

    def get_max_bid(self):
        return self.__max_bid

    def set_max_bid(self, bid: Bid):
        self.__max_bid = bid

    def get_was_sold(self):
        return self.__was_sold

    def set_was_sold(self, was_sold):
        self.__was_sold = was_sold

    def return_bidders(self):
        return 'Max Bid:' + str(self.__max_bid.get_price()) + ' Bidder: ' + \
            self.__max_bid.get_bidder() if self.__max_bid is not None else ''

    def __str__(self):
        return f"Name: {self.__name} Starting Price: {str(self.__starting_price)} Was Sold: {self.__was_sold} {self.return_bidders()}"
