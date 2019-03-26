import socket
import threading
import sys


class Server:
    class Client:
        def __init__(self, sock, addr):
            self.sock = sock
            self.addr = addr

        def __str__(self):
            return "[" + self.addr[0] + "]==[" + str(self.addr[1]) + "]"

    class Game:
        def __init__(self, server, client1, client2, id):
            self.client1 = client1
            self.client2 = client2
            self.move_data = ""
            self.cur_listened_client = None
            self.stop_game = False
            self.server = server
            self.id = id

        def client_thread(self, client):
            while not self.stop_game:
                try:
                    data = client.sock.recv(1024)

                    if self.cur_listened_client == client:
                        self.move_data = data.decode("utf-8")
                except Exception as ex:
                    print(ex)
                    self.stop_game = True

        def OtherClient(self, client):
            if client == self.client1:
                return self.client2
            else:
                return self.client1

        def start_game_procedure(self):
            threading.Thread(target=self.client_thread, args=(self.client1,)).start()
            threading.Thread(target=self.client_thread, args=(self.client2,)).start()

            self.cur_listened_client = self.client1

            print("Game " + str(self.id) + " started")
            Server.send_message(self.cur_listened_client, "Your turn...")

        def stop_game_procedure(self):
            self.client1.sock.close()
            self.client2.sock.close()
            print("Game " + str(self.id) + " stopped")
            self.server.cnt_games -= 1

        def run(self):
            self.start_game_procedure()
            while not self.stop_game:
                if self.move_data == "":
                    continue

                move_info = str(self.cur_listened_client) + "==[Game id: " + \
                            str(self.id) + "]: " + self.move_data
                print(move_info)

                other_client = self.OtherClient(self.cur_listened_client)
                Server.send_message(other_client, move_info + "\n Your turn...")
                self.cur_listened_client = other_client
                self.move_data = ""

            self.stop_game_procedure()


    def __init__(self, port=9090):
        host = socket.gethostbyname(socket.gethostname())

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, port))
            print("Socket Bound to port " + str(port))
        except Exception as ex:
            print("Socket creation failed:")
            print(ex)
            sys.exit(0)

        self.sock.listen(2)
        self.clients = []
        self.cnt_games = 0

    @staticmethod
    def send_message(client, message):
        client.sock.sendall(message.encode("utf-8"))

    def match_making_procedure(self, client):
        if client not in self.clients:
            self.clients.append(client)

        if len(self.clients) == 2:
            self.cnt_games += 1
            game = Server.Game(self, self.clients[0], self.clients[1], self.cnt_games)
            threading.Thread(target=game.run).start()
            self.clients.clear()

    def run(self):
        while True:
            try:
                sock, addr = self.sock.accept()
                client = Server.Client(sock, addr)

                Server.send_message(client, "Connection successfull!")
                print("Connected to: " + str(client))

                self.match_making_procedure(client)

            except Exception as ex:
                print(ex)
                break
        self.sock.close()

Server().run()