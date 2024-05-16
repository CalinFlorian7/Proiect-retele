class UserRegistry:
    __users = {}

    def __init__(self):
        self.__users = {}

    def get_users(self):
        return self.__users

    def add_user(self, user):
        if user.get_name() not in self.__users:
            self.__users[user.get_name()] = user

    def remove_user(self, username):
        if username in self.__users:
            del self.__users[username]

    def username_exists(self, username):
        if username in self.__users:
            return True
        else:
            return False

    # def addProductForUser(self, username, product):
    #     if username in self.__users:
    #         error = self.__users[username].addProduct(product)
    #         if error is not None:
    #             return error
    #     else:
    #         print(f"User {username} does not exist")

    # def updateProductFinalPrice(self, userName, productName, updatedPrice):
    #     if userName in self.__users:
    #         userCurrent = self.__users[userName]
    #         products = userCurrent.getProducts()

    #         if productName in products:
    #             if products[productName].getStartingPrice() >= updatedPrice:
    #                 return f"Price {updatedPrice} is lower than the starting price {products[productName].getStartingPrice()}"
    #             elif products[productName].getFinalPrice() >= updatedPrice:
    #                 return f"Price {updatedPrice} is lower than the final price {products[productName].getFinalPrice()}"
    #             else:
    #                 products[productName].setFinalPrice(updatedPrice)
    #         else:
    #             return f"Product {productName} does not exist for user {userName}"
    #     else:
    #         return f"User {userName} does not exist"

    # def getProductsForUser(self, userName):
    #     if userName in self.__users:
    #         userCurrent = self.__users[userName]
    #         return userCurrent.getProducts()
    #     return f"User {userName} does not exist"

    # def displayUsers(self):
    #     print("Users already added:")
    #     for userName in self.__users:
    #         userCurent = self.__users[userName]
    #         userCurent.displayUserProducts()
