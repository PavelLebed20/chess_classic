###############################
# MODULE: Obtain functions    #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 08/04/2019     #
###############################
import ChessRender.UIPrimitives.object_manage as om
import ChessRender.UIPrimitives.text_field as tf
import ChessRender.UIPrimitives.button as bu

from Vector2d.Vector2d import Move, Vector2d

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

def exit_fun(render):
    render.userExit()

def game_fun(render):
    render.state = om.RenderState.GAME
    render.need_init = True
    clear_fun(render)

def main_menu(render):
    render.state = om.RenderState.MENU
    clear_fun(render)
    global buttons_arr
    buttons_arr = [bu.Button(Vector2d(0, 10), game_fun, title="Start game"),
                   bu.Button(Vector2d(0, 5), online_fun, title="Online game"),
                   bu.Button(Vector2d(0, 0), exit_fun, title="Exit")]
    global text_fields_arr
    text_fields_arr = None

def online_fun(render):
    render.state = om.RenderState.MENU
    clear_fun(render)
    global buttons_arr
    buttons_arr = [bu.Button(Vector2d(0, -5), main_menu, title="Back"),
                   bu.Button(Vector2d(0, 0), find_player_fun, title="Next")]
    global text_fields_arr
    text_fields_arr = [tf.TextField(Vector2d(0, 10), title="Login"),
                        tf.TextField(Vector2d(0, 5), title="Parol")]

def find_player_fun(render):
    render.state = om.RenderState.MENU
    clear_fun(render)
    global buttons_arr
    buttons_arr = [bu.Button(Vector2d(0, -5), main_menu, title="Back"),
                   bu.Button(Vector2d(0, 0), game_fun, title="Next")]
    global text_fields_arr
    text_fields_arr = [tf.TextField(Vector2d(-7, 10), title="Game time",
                                    size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y)),
                       tf.TextField(Vector2d(7, 10), title="Move time",
                                    size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y)),
                       tf.TextField(Vector2d(-7, 5), title="Min. rate",
                                     size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y)),
                       tf.TextField(Vector2d(7, 5), title="Max. rate",
                                     size=Vector2d(tf.MINI_SCALE_X, tf.TEXT_FIELD_SCALE_Y))]

buttons_arr =  None
text_fields_arr = None
