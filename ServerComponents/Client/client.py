import socketio
import threading


class Client:
    def __init__(self, adress):
        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)

        self.sio.connect(adress)

        threading.Thread(target=self.listen, daemon=True).start()

        self.sio.emit('message', "SOSI XYI")

    def listen(self):
        self.sio.wait()

    def send_message(self, event, data):
        self.sio.emit(event, data)

    def on_message(self, data):
        print('Recieved message: ' + str(data))

    def on_connect(self):
        print('Connection established')

    def on_disconnect(self):
        print('Disconnected from server')
