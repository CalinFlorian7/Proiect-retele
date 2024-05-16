class User:
    def __init__(self, name, client_socket):
        self.__name = name
        self.__client_socket = client_socket

    def get_name(self):
        return self.__name

    def get_client_socket(self):
        return self.__client_socket

    def __str__(self):
        return f"Name: {self.__name} Client Socket: {self.__client_socket}"

    def addProduct(self):
        pass

    def getProducts(self):
        pass

    def displayUserProducts(self):
        pass
