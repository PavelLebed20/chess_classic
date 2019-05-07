import socketio
import threading

import ServerComponents.Suppurt.support as supp


class Client:
    def __init__(self, adress, on_login_call, on_update_call, on_update_time_call, on_avail_packs_call):
        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)
        self.sio.on('login', self.on_login)
        self.sio.on('update_game', self.on_update_board)
        self.sio.on('update_time', self.on_update_time)
        self.sio.on('avail_packs', self.on_avail_packs)

        self.on_update_call = on_update_call
        self.on_login_call = on_login_call
        self.on_update_time_call = on_update_time_call
        self.on_avail_packs_call = on_avail_packs_call

        try:
            self.sio.connect(adress)
        except:
            print("can't connect to server")
            return

        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        self.sio.wait()

    def send_message(self, event, data):
        self.sio.emit(event, data)

    def on_avail_packs(self, data):
        paramsMap = supp.getParamsValMap(data)
        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))
        if self.on_avail_packs_call is not None:
            self.on_avail_packs_call(paramsMap['packs'])



    def on_login(self, params_data):
        paramsMap = supp.getParamsValMap(params_data)
        print('Recieved message: ' + str(params_data) + ' ' + paramsMap['request_id'])

        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))
        #####
        if self.on_login_call is not None:
            self.on_login_call(paramsMap)

    def on_update_board(self, params_data):
        paramsMap = supp.getParamsValMap(params_data)
        print('Recieved message: ' + str(params_data) + ' ' + paramsMap['request_id'])

        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))
        #####
        if self.on_update_call is not None:
            self.on_update_call(paramsMap)

    def on_update_time(self, params_data):
        paramsMap = supp.getParamsValMap(params_data)
        print('Recieved message: ' + str(params_data) + ' ' + paramsMap['request_id'])
        self.sio.emit('verify_message', "request_id={}".format(paramsMap['request_id']))
        #####
        if self.on_update_time_call is not None:
            self.on_update_time_call(paramsMap)

    def on_message(self, data):
        print('Recieved message: ' + str(data))

    def on_connect(self):
        print('Connection established')

    def on_disconnect(self):
        self.sio.emit('disconnect', "")
        print('Disconnected from server')

