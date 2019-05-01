
# database and gamecontroller imports
import json

import ServerComponents.Suppurt.support as supp
import pickle
import ChessAI.GameController.game_controller as game_controller
import Vector2d.Vector2d as vec
import psycopg2
import ast

# server connection
import eventlet

from ChessBoard.chess_board import Board

eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
usersAddr = {}

clients = {}
none_messages = {}
con_sync = supp.db().con
con_async = supp.db().con
class Server:

    def __init__(self, port):
        self.port = port

    def run(self):
        cursor = con_sync.cursor()
        cursor.execute("call chess.start_server()")
        con_sync.commit()
        cursor.close()
        socketio.start_background_task(self.message_queue_processing)
        socketio.run(app, port=self.port)

    def message_queue_processing(self):
        while True:
            cursor = con_async.cursor()
            cursor.execute("select chess.get_request()")
            rec_id = cursor.fetchone()[0]
            cursor.execute("select * from chess.get_messages({})".format(rec_id))
            records = cursor.fetchall()
            for rec in records:
                user_id = int(rec[0])
                actionToParams = str(rec[1]).split('?')
                action = actionToParams[0]
                params = actionToParams[1]
                user_sid = supp.getkeyByVal(clients, user_id)

                # fill none messages
                if (user_sid is None):
                    none_messages[user_id][0] = action
                    none_messages[user_id][1] = params
                else:
                    print("user id is: " + str(user_id))
                    print("user SID is: " + str(user_sid))
                    print("action is " + str(action))
                    print("params is " + str(params))

                    socketio.emit(action, params, room=user_sid)

            #send none messages to not NONE clients
            for user_id in none_messages:
                user_sid = supp.getkeyByVal(clients, user_id)
                if (user_sid is not None):
                    print("user id is: " + str(user_id))
                    print("user SID is: " + str(user_sid))
                    print("action is " + str(none_messages[user_id][0]))
                    print("params is " + str(none_messages[user_id][1]))
                    socketio.emit(none_messages[user_id][0], none_messages[user_id][1], room=user_sid)
                    del none_messages[user_id]

            con_async.commit()
            cursor.close()

@socketio.on('connect')
def on_connect():
    print("%s connected" % (request.sid))
    clients[request.sid] = None

@socketio.on('disconnect')
def on_disconnect():
    print("%s disconnected" % (request.sid))
    cursor = con_sync.cursor()
    if (clients[request.sid] is not None):
        cursor.execute("call chess.on_disconnect({0})".format(clients[request.sid]))
    con_sync.commit()
    cursor.close()
    clients.pop(request.sid)

@socketio.on('verify_message')
def on_verify_message(data):
    print("Message recieved: " + str(data) + "from client " + str(clients[request.sid]))

    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()
    if (clients[request.sid] is not None):
        cursor.execute("call chess.verify_message({0}, {1})".format(paramsDict['request_id'], clients[request.sid]))
    con_sync.commit()
    cursor.close()

@socketio.on('confirm_auth')
def on_confirm_auth(data):
    print("Message recieved: " + str(data))

    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()

    cursor.execute("select chess.confirm_auth('{0}', '{1}')".format(paramsDict['email'],
                                                                    paramsDict['auth_code']))

@socketio.on('auth')
def on_auth(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()

    cursor.execute("select chess.auth('{0}', '{1}', '{2}')".format(paramsDict['login'], paramsDict['email'],
                                                                   paramsDict['password']))

@socketio.on('login')
def on_login(data):
    print("Message recieved: " + str(data))

    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()

    cursor.execute("select chess.login('{0}', '{1}')".format(paramsDict['login'], paramsDict['password']))
    # set user_id for session
    print("login SID is " + str(request.sid))
    clients[request.sid] = cursor.fetchone()[0]
    print("login ID is " + str(clients[request.sid]))
    con_sync.commit()
    cursor.close()

@socketio.on('find_pair')
def on_find_pair(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()
    if (clients[request.sid] is not None):
        cursor.execute("call chess.find_pair({0}, {1}, {2}, {3},"
                   " p_game_time := TIME '00:0{4}:00')".format
                   (clients[request.sid], paramsDict['low_rate'], paramsDict['hight_rate'],
                    paramsDict['move_time'], paramsDict['game_time']))

    con_sync.commit()
    cursor.close()

@socketio.on('update_board')
def on_update_board(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()

    # get board from database
    if (clients[request.sid] is not None):
        cursor.execute("select chess.get_current_game_board({0})".format(clients[request.sid]))
    rec = cursor.fetchone()[0]
    #print("server_board is " + str(rec))
    # convert to game_controller
    if (rec is not None):
        cur_game_controller = game_controller.GameController(None, str(rec))
    else:
        cur_game_controller = game_controller.GameController(Board())

    move = vec.Move(vec.Vector2d(int(paramsDict['p1']), int(paramsDict['p2'])),
                    vec.Vector2d(int(paramsDict['p3']), int(paramsDict['p4'])))

    #res = cur_game_controller.check_move(move)
    #if (res != game_controller.MoveResult.INCORRECT):

    cur_game_controller.update(move)

    cursor.execute("call chess.update_game_state({0}, '{1}')".format(clients[request.sid],
                                                                   cur_game_controller.serialize_to_str()))

    con_sync.commit()
    cursor.close()

@socketio.on('message')
def on_message(data):
    print("Message recieved: " + str(data))
    socketio.emit('message', 'Response from server')


server = Server(8000)
server.run()
