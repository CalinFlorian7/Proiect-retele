from src.server.Server import Server

from src.constants.constants import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()
