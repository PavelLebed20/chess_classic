import socket, threading, time


class Client:
    def __init__(self, host, port=9090):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = (host, port)
        self.sock.connect(self.server)

    @staticmethod
    def receive_thread(sock):
        while True:
            try:
                data = sock.recv(1024)

                if data:
                    print(data.decode("utf-8"))

                time.sleep(0.2)
            except Exception as ex:
                print(ex)
                break
        sock.close()

    def send_message(self, message):
        self.sock.sendto(message.encode("utf-8"), self.server)

    def start_receiving(self):
        threading.Thread(target=Client.receive_thread, args=(self.sock,)).start()

        while True:
            try:
                message = input()

                if message != "":
                    self.sock.sendto(message.encode("utf-8"), self.server)

                time.sleep(0.2)
            except Exception as ex:
                print(ex)
                break


Client(host=socket.gethostbyname(socket.gethostname())).run()