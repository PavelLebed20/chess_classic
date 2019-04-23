
# database and gamecontroller imports
import ServerComponents.Suppurt.support as supp
import pickle
import ChessAI.GameController.game_controller as game_controller
import Vector2d.Vector2d as vec
import time
import ast

# server connection
import eventlet
eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
usersAddr = {}

class Server:
    clients = {}
    con_sync = supp.db().con
    con_async = supp.db().con

    def __init__(self, port):
        self.port = port

    def run(self):
        socketio.start_background_task(self.message_queue_processing)
        socketio.run(app, port=self.port, debug=True)

    def message_queue_processing(self):
        while True:
            cursor = self.con_async.cursor()
            cursor.execute("select chess.get_request()")
            rec_id = cursor.fetchone()[0]
            cursor.execute("select chess.get_messages({})".format(rec_id))
            records = cursor.fetchall()
            for rec in records:
                user_id_to_action = rec[0].split(',')
                user_id = int(str(user_id_to_action[0][1:]))
                actionToParams = user_id_to_action[1][:-1].split('?')
                action = actionToParams[0]
                user_sid = supp.getkeyByVal(Server.clients, user_id)

                print("user id is: " + str(user_id))
                print("session id is: " + str(user_sid))
                print("action is: " + str(action))
                print("action params is: " + str(actionToParams[1]))

                socketio.emit(action, actionToParams[1], room=user_sid)
            time.sleep(0.05)
            Server.con_async.commit()
            cursor.close()

@socketio.on('connect')
def on_connect():
    print("%s connected" % (request.sid))
    Server.clients[request.sid] = None

@socketio.on('disconnect')
def on_disconnect():
    print("%s disconnected" % (request.sid))
    Server.clients.pop(request.sid)
    cursor = Server.con_sync.cursor()

    #cursor.execute(
    #    "".format(Server.clients[request.sid]))
    Server.con_sync.commit()
    cursor.close()


@socketio.on('verify_message')
def on_verify_message(data):
    print("Message recieved: " + str(data) + "from client " + str(Server.clients[request.sid]))

    paramsDict = supp.getParamsValMap(data)
    cursor = Server.con_sync.cursor()

    cursor.execute("call chess.verify_message('{0}', '{1}')".format(paramsDict['request_id'], Server.clients[request.sid]))
    Server.con_sync.commit()
    cursor.close()

@socketio.on('login')
def on_login(data):
    print("Message recieved: " + str(data))

    paramsDict = supp.getParamsValMap(data)
    cursor = Server.con_sync.cursor()

    cursor.execute("select chess.login('{0}', '{1}')".format(paramsDict['login'], paramsDict['password']))
    # set user_id for session
    Server.clients[request.sid] = cursor.fetchone()[0]
    Server.con_sync.commit()
    cursor.close()

@socketio.on('find_pair')
def on_find_pair(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    cursor = Server.con_sync.cursor()

    cursor.execute("call chess.find_pair({0}, {1}, {2}, {3},"
                   " p_game_time := TIME '00:0{4}:00')".format
                   (Server.clients[request.sid], paramsDict['low_rate'], paramsDict['hight_rate'],
                    paramsDict['move_time'], paramsDict['game_time']))

    Server.con_sync.commit()
    cursor.close()

@socketio.on('update_board')
def on_update_board(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    cursor = Server.con_sync.cursor()

    # get board from database
    cursor.execute("call chess.get_current_game_board({0})".format(Server.clients[request.sid]))
    rec = cursor.fetchone()
    print("cur_game_board is: " + str(rec))
    # convert to game_controller
    cur_game_controller = game_controller.GameController(pickle.loads(rec))
    move = vec.Move(vec.Vector2d(paramsDict['p1'], paramsDict['p2']),
                    vec.Vector2d(paramsDict['p3'], paramsDict['p4']))

    res = cur_game_controller.check_move(move)
    # update board
    if (res != game_controller.MoveResult.INCORRECT):
        cur_game_controller.update(move)

    cursor.execute("call chess.update_game_board({0}, '{1}')".format(Server.clients[request.sid], cur_game_controller))

    Server.con_sync.commit()
    cursor.close()

@socketio.on('message')
def on_message(data):
    print("Message recieved: " + str(data))
    socketio.emit('message', 'Response from server')


server = Server(8000)
server.run()
