
# database and gamecontroller imports
import json
import smtplib

from validate_email import validate_email

import ServerComponents.Suppurt.support as supp
import ChessAI.GameController.game_controller as game_controller
import Vector2d.Vector2d as vec


# server connection
import eventlet

from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side

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

# email data
#server.starttls()
#server.login("chess.classic.official@gmail.com", "ChhessClassicc1488")


class Server:

    def __init__(self, port):
        self.port = port

    def run(self):
        cursor = con_sync.cursor()
        cursor.execute("call chess.start_server()")
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
                print(none_messages)
                user_sid = supp.getkeyByVal(clients, user_id)
                if (user_sid is not None):
                    print("user id is: " + str(user_id))
                    print("user SID is: " + str(user_sid))
                    print("action is " + str(none_messages[user_id][0]))
                    print("params is " + str(none_messages[user_id][1]))
                    socketio.emit(none_messages[user_id][0], none_messages[user_id][1], room=user_sid)
                    del none_messages[user_id]

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

    cursor.close()
    clients.pop(request.sid)

@socketio.on('verify_message')
def on_verify_message(data):
    print("Message recieved: " + str(data) + "from client " + str(clients[request.sid]))

    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()
    if (clients[request.sid] is not None):
        cursor.execute("call chess.verify_message({0}, {1})".format(paramsDict['request_id'], clients[request.sid]))

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
    print("Parsed params: " + str(paramsDict))

    if not validate_email(paramsDict['email']):
        return

    cursor = con_sync.cursor()

    cursor.execute("select chess.registrate('{0}', '{1}', '{2}')".format(paramsDict['login'],
                                                                         paramsDict['password'],
                                                                         paramsDict['email']))
    res = cursor.fetchone()[0]
    print(str(res))

    print("Auth code is " + str(res))
    if res is not None:
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login("chess.classic.official@gmail.com", "ChhessClassicc1488")
            msg = "{0}, thank your for authorization on chess classic club.".format(paramsDict['login'])
            msg += "Your authentication code is {0}.".format(res)

            server.sendmail("chess.classic.official@gmail.com", [paramsDict['email']], msg)
            server.quit()
        except:
            print('Failed to send email to {}'.format(paramsDict['email']))


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


    cursor.close()

@socketio.on('update_board')
def on_update_board(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    cursor = con_sync.cursor()

    # get board from database
    if clients[request.sid] is not None:
        cursor.execute("select * from chess.get_current_game_board_state({0})".format(clients[request.sid]))
    else:
        return
    try:
       rec = cursor.fetchone()
       print("Game state is " + str(rec))
       board = rec[0]
       side = int(rec[1])
    except:
        cursor.close()
        print("Game doesn't exists")
        return
    #print("server_board is " + str(rec))
    # convert to game_controller
    print("Board is " + str(board))
    print("Side is " + str(side))
    if board is not None:
        cur_game_controller = game_controller.GameController(None, str(board))
    else:
        cur_game_controller = game_controller.GameController(Board())

    move = vec.Move(vec.Vector2d(int(paramsDict['p1']), int(paramsDict['p2'])),
                    vec.Vector2d(int(paramsDict['p3']), int(paramsDict['p4'])))

    res = cur_game_controller.check_move(move, Side(side))
    if res == game_controller.MoveResult.INCORRECT:
        print("Wrong move send")
        cursor.close()
        return


    cur_game_controller.update(move)

    cursor.execute("call chess.update_game_state({0}, '{1}')".format(clients[request.sid],
                                                                   cur_game_controller.serialize_to_str()))


    cursor.close()

@socketio.on('message')
def on_message(data):
    print("Message recieved: " + str(data))
    socketio.emit('message', 'Response from server')


server = Server(8000)
server.run()
