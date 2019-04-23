import socketio
import threading

import ServerComponents.Suppurt.support as supp

class Client:
    def __init__(self, adress, on_login_call, on_update_call):
        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.on('login', self.on_login)
        self.sio.on('update_game', self.on_update_board)

        self.on_update_call = on_update_call
        self.on_login_call = on_login_call

        self.sio.connect(adress)
        threading.Thread(target=self.listen, daemon=True).start()

        self.sio.emit('message', "I'm here)))")

    def listen(self):
        self.sio.wait()

    def send_message(self, event, data):
        self.sio.emit(event, data)

    def on_login(self, data):
        paramsMap = data
        print('Recieved message: ' + str(data) + ' ' +paramsMap['request_id'])

        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))
        #####
        if self.on_login_call is not None:
            self.on_login_call(paramsMap)

    def int_to_bytes(self, value, len):
        res = []

        for i in len:
            res.append(value >> (i * 8) & 0xff)

        res.reverse()
        return res

    def on_update_board(self, params_data):
        paramsMap = params_data
        print('Recieved message: ' + str(params_data) + paramsMap['request_id'])

        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))
        #####
        if self.on_update_call is not None:
            if paramsMap['game_controller_bytea'] is not None:
                paramsMap['game_controller_bytea'] = self.int_to_bytes(paramsMap['game_controller_bytea'],
                                                                       paramsMap['len'])
            self.on_update_call(paramsMap)

    def on_message(self, data):
        print('Recieved message: ' + str(data))

    def on_connect(self):
        print('Connection established')

    def on_disconnect(self):
        self.sio.emit('disconnect', "")
        print('Disconnected from server')
