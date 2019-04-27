###############################
# MODULE: Obtain functions    #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 08/04/2019     #
###############################
import ChessRender.UIPrimitives.object_manage as om
import ChessRender.UIPrimitives.text_field as tf
import ChessRender.UIPrimitives.button as bu
import ChessRender.UIPrimitives.room as rm
import ChessRender.load_models as lm

from Vector2d.Vector2d import Vector2d

def clear_fun(render):
    if render.button_arr is not None:
        for b in render.button_arr:
            b[bu.OBJECT_I].removeNode()
            b[bu.TEXT_I].removeNode()
        render.button_arr = None

    if render.text_field_arr is not None:
        for b in render.text_field_arr:
            b[tf.OBJECT_I].removeNode()
            b[tf.TEXT_I].removeNode()
            b[tf.TEXT_PRINT_I].removeNode()
        render.text_field_arr = None

    render.room.state = rm.RoomState.DEFAULT

def exit_fun(render):
    render.userExit()

def game_fun(render):
    render.state = om.RenderState.GAME
    render.need_init = True
    render.room.state = rm.RoomState.GAME
    clear_fun(render)


def main_menu(render):
    render.state = om.RenderState.MENU
    clear_fun(render)
    render.room.buttons_prim = [bu.Button(Vector2d(0, 10), render.process_offline_game, title="Start game"),
                   bu.Button(Vector2d(0, 5), online_fun, title="Online game"),
                   bu.Button(Vector2d(0, 0), registr_fun, title="Registration"),
                   bu.Button(Vector2d(0, -5),  lm.go_to_load_model_menu_fun, title="Load models"),
                   bu.Button(Vector2d(0, -10), exit_fun, title="Exit"),
                                ]

    render.room.text_fields_prim = None

    render.room.state = rm.RoomState.MAIN_MENU

def online_fun(render):
    render.state = om.RenderState.MENU
    clear_fun(render)

    render.room.buttons_prim = [bu.Button(Vector2d(0, -5), main_menu, title="Back"),
                   bu.Button(Vector2d(0, 0), render.room.process_data, title="Next")]

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 10), title=rm.L_LOGIN),
                        tf.TextField(Vector2d(0, 5), title=rm.L_PAROL)]

    render.room.state = rm.RoomState.LOGIN_MENU

def registr_fun(render):
    render.state = om.RenderState.MENU
    clear_fun(render)

    render.room.buttons_prim = [bu.Button(Vector2d(0, -10), main_menu, title="Back"),
                   bu.Button(Vector2d(0, -5), render.room.process_data, title="Next")]

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 10), title=rm.L_LOGIN),
                        tf.TextField(Vector2d(0, 5), title=rm.L_PAROL),
                        tf.TextField(Vector2d(0, 0), title=rm.L_EMAIL)]

    render.room.state = rm.RoomState.REGISTRATION_MENU

def find_player_fun(render):
    #### - get values from text fields
    render.state = om.RenderState.MENU
    clear_fun(render)

    render.room.buttons_prim = [bu.Button(Vector2d(0, -5), main_menu, title="Back"),
                   bu.Button(Vector2d(0, 0), render.room.process_data, title="Next")]

    render.room.text_fields_prim = [tf.TextField(Vector2d(-7, 10), title=rm.L_GAME_TIME,
                                    size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y)),
                       tf.TextField(Vector2d(7, 10), title=rm.L_MOVE_TIME,
                                    size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y)),
                       tf.TextField(Vector2d(-7, 5), title=rm.L_MIN_RATE,
                                     size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y)),
                       tf.TextField(Vector2d(7, 5), title=rm.L_MAX_RATE,
                                     size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y))]

    render.room.state = rm.RoomState.FIND_PLAYER_MENU

def game_online_fun(render):
    render.state = om.RenderState.GAME
    render.need_init = True
    render.room.state = rm.RoomState.GAME
    clear_fun(render)
