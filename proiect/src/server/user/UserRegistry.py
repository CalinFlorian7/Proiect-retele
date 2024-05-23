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

   