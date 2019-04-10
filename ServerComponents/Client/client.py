import socketio
import threading

import ServerComponents.Suppurt.support as supp

class Client:
    def __init__(self, adress):
        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.on('login', self.on_login)
        self.sio.on('find_pair', self.on_find_pair)
        self.sio.on('update_board', self.on_update_board)

        self.sio.connect(adress)
        threading.Thread(target=self.listen, daemon=True).start()

        self.sio.emit('message', "I'm here)))")

    def listen(self):
        self.sio.wait()

    def send_message(self, event, data):
        self.sio.emit(event, data)

    def on_login(self, data):
        paramsMap = supp.getParamsValMap(str(data))
        print('Recieved message: ' + str(data) + ' ' +paramsMap['request_id'])

        #####
        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))

    def on_update_board(self, data):
        paramsMap = supp.getParamsValMap(str(data))
        print('Recieved message: ' + str(data) + paramsMap['request_id'])

        #####
        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))

    def on_find_pair(self, data):
        print('Recieved message: ' + str(data))
        # verify message
        paramsMap = supp.getParamsValMap(data)

        ###
        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))

    def on_message(self, data):
        print('Recieved message: ' + str(data))

    def on_connect(self):
        print('Connection established')

    def on_disconnect(self):
        print('Disconnected from server')
