from src.client.client import Client

from src.constants.constants import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect()
