class Bid:

    __price: float
    __bidder: str

    def __init__(self, price, bidder):
        self.__price = price
        self.__bidder = bidder

    def get_price(self):
        return self.__price

    def get_bidder(self):
        return self.__bidder

    def __str__(self):
        return f"{self.__bidder} bid {self.__price}"
