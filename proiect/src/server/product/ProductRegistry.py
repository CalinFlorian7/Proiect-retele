from src.server.product.Product import Product
from src.server.user.User import User


class ProductRegistry:
    __products = {}

    def __init__(self):
        self.__products = {}

    def get_products(self):
        return self.__products

    def get_user_products(self, user: User):
        if user.get_name() not in self.__products:
            self.__products[user.get_name()] = []
        return self.__products[user.get_name()]

    def add_product(self, user: User, product: Product):
        if user.get_name() not in self.__products:
            self.__products[user.get_name()] = []
        self.__products[user.get_name()].append(product)

    def is_product_registered(self, user: User, product: Product):
        products = self.get_user_products(user)
        for prod in products:
            if prod.get_name() == product.get_name():
                print("Product registered")
                return True
        return False

    def remove_user_products(self, username):
        if username in self.__products:
            del self.__products[username]

   