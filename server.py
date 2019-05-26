# database and gamecontroller imports

import smtplib
from time import sleep

from validate_email import validate_email

import ServerComponents.Suppurt.support as supp
import ChessAI.GameController.game_controller as game_controller
import Vector2d.Vector2d as vec

# server connection
import eventlet

from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side
from ServerComponents.Suppurt.server import execute_no_res_async, execute_one_res_async, execute_all_res_async
from message_sender import send_email

eventlet.monkey_patch()
from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
usersAddr = {}

clients = {}
user_client_map = {}
messages = {}


# email data
# server.starttls()
# server.login("chess.classic.official@gmail.com", "ChhessClassicc1488")


class Server:

    def __init__(self, port):
        self.port = port

    def run(self):
        execute_no_res_async("call chess.start_server()")
        socketio.start_background_task(self.message_queue_processing)
        socketio.run(app, port=self.port)

    def message_queue_processing(self):
        while True:
            rec_id = execute_one_res_async("select chess.get_request()")[0]
            records = execute_all_res_async("select * from chess.get_messages({})".format(rec_id))
            for rec in records:
                user_id = int(rec[0])
                action_to_params = str(rec[1]).split('?')
                action = action_to_params[0]
                params = action_to_params[1]
                user_sid = user_client_map.get(user_id, None)

                # fill none messages
                if user_sid is not None:
                    print("user id is: " + str(user_id))
                    print("user SID is: " + str(user_sid))
                    print("action is " + str(action))
                    print("params is " + str(params))
                    socketio.emit(action, params, room=user_sid)

            execute_no_res_async('call chess.run_jobs()')


@socketio.on('connect')
def on_connect():
    print("%s connected" % (request.sid))
    if request.sid in clients and clients[request.sid] is not None:
        user_client_map[clients[request.sid]] = None
    clients[request.sid] = None


@socketio.on('disconnect')
def on_disconnect():
    print("%s disconnected" % (request.sid))
    if request.sid in clients and clients[request.sid] is not None:
        query = "call chess.on_disconnect({0})".format(clients[request.sid])
        execute_no_res_async(query)


@socketio.on('verify_message')
def on_verify_message(data):
    # print("Message recieved: " + str(data) + "from client " + str(clients[request.sid]))

    paramsDict = supp.getParamsValMap(data)
    if request.sid in clients and clients[request.sid] is not None:
        query = "call chess.verify_message({0}, {1})".format(paramsDict['request_id'], clients[request.sid])
        execute_no_res_async(query)


@socketio.on('confirm_auth')
def on_confirm_auth(data):
    print("Message recieved: " + str(data))

    paramsDict = supp.getParamsValMap(data)

    query = "select chess.confirm_auth('{0}', '{1}')".format(paramsDict['email'],
                                                           paramsDict['auth_code'])
    res = int(execute_one_res_async(query))
    if res == 0:
        # send error message
        socketio.emit('error', 'message=wrong auth code or email', room=request.sid)



@socketio.on('auth')
def on_auth(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    print("Parsed params: " + str(paramsDict))

    if not validate_email(paramsDict['email']):
        return

    query = "select chess.registrate('{0}', '{1}', '{2}')".format(paramsDict['login'],
                                                                  paramsDict['password'],
                                                                  paramsDict['email'])

    res = execute_one_res_async(query)[0]
    if res == "":
        # send error message
        socketio.emit('error', 'message=Wrong registration params', room=request.sid)


@socketio.on('login')
def on_login(data):
    print("Message recieved: " + str(data))

    paramsDict = supp.getParamsValMap(data)

    query = "select chess.login('{0}', '{1}')".format(paramsDict['login'], paramsDict['password'])
    # set user_id for session
    print("login SID is " + str(request.sid))
    user_id = int(execute_one_res_async(query)[0])
    if user_id < 0:
        print('Invalid user!')
        # send error message
        socketio.emit('error', 'message=Unknown login or password', room=request.sid)
        return
    clients[request.sid] = user_id
    user_client_map[user_id] = request.sid
    print("login ID is " + str(clients[request.sid]))


@socketio.on('find_pair')
def on_find_pair(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)
    if request.sid in clients and clients[request.sid] is not None:
        query = "call chess.find_pair({0}, {1}, {2}, {3}," \
                " p_game_time := TIME '00:{4}:00')".format(clients[request.sid],
                                                           int(paramsDict['low_rate']),
                                                           int(paramsDict['hight_rate']),
                                                           int(paramsDict['move_time']),
                                                           str(paramsDict['game_time']).rjust(2, '0'))
        execute_no_res_async(query)


@socketio.on('find_pair_list')
def on_find_pair_list(data):
    print("Message recieved: " + str(data))
    if request.sid in clients and clients[request.sid] is not None:
        query = "call chess.add_pairings_list({0})".format(clients[request.sid])
        execute_no_res_async(query)


@socketio.on('start_game_by_pairing')
def on_find_pair_list(data):
    paramsDict = supp.getParamsValMap(data)
    print("Message recieved: " + str(data))
    if request.sid in clients and clients[request.sid] is not None:
        query = "call chess.start_game_by_pairing_id({0}, {1})".format(clients[request.sid], paramsDict['pairing_id'])
        execute_no_res_async(query)


@socketio.on('update_board')
def on_update_board(data):
    print("Message recieved: " + str(data))
    paramsDict = supp.getParamsValMap(data)

    # get board from database
    if clients[request.sid] is not None:
        query = "select * from chess.get_current_game_board_state({0})".format(clients[request.sid])
    else:
        return
    try:
        rec = execute_one_res_async(query)
        print("Game state is " + str(rec))
        board = rec[0]
        side = int(rec[1])
    except:
        print("Game doesn't exists")
        return
    # print("server_board is " + str(rec))
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
        return

    is_playing = 1
    game_result = None
    pawn_swaped_figure = paramsDict['swapped_figure']

    print('Swaped figure is ' + str(pawn_swaped_figure))

    cur_game_controller.update(move, Side(side))

    if pawn_swaped_figure is not None:
        cur_game_controller.swap_pawn(move.point_to, pawn_swaped_figure)
        res = cur_game_controller.check_board_res(Side(side))

    if res == game_controller.MoveResult.STALEMATE:
        is_playing = 0
    elif res == game_controller.MoveResult.MATE:
        is_playing = 0
        game_result = 0 if Side(side) is Side.WHITE else 1

    if game_result is None:
        execute_no_res_async("call chess.update_game_state({0}, '{1}', "
                             "{2}::bit, NULL)".format(clients[request.sid],
                                                      cur_game_controller.serialize_to_str(),
                                                      is_playing))
    else:
        execute_no_res_async("call chess.update_game_state({0}, '{1}', "
                             "{2}::bit, {3}::bit)".format(clients[request.sid],
                                                          cur_game_controller.serialize_to_str(),
                                                          is_playing,
                                                          game_result))


@socketio.on('update_pack')
def on_update_pack(data):
    print("Message recieved: " + str(data))
    params_dict = supp.getParamsValMap(data)
    if request.sid in clients and clients[request.sid] is not None:
        try:
            query = "call chess.update_pack({0}, '{1}')" \
                    "".format(clients[request.sid], params_dict['pack_name'])
            print('query is ' + query)
            execute_no_res_async(query)
        except:
            print("Error while update pack")


@socketio.on('message')
def on_message(data):
    print("Message recieved: " + str(data))
    socketio.emit('message', 'Response from server')


server = Server(8000)
server.run()
