import ChessRender.UIPrimitives.object_manage as om
import ChessRender.UIPrimitives.text_field as tf
import ChessRender.UIPrimitives.button as bu
import ChessRender.obtain_functions as of
from Vector2d.Vector2d import Vector2d


def load_king(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.append('k')

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -10), go_to_load_model_menu_fun, title="Back")
        ]


def load_queen(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.append('q')

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -5), go_to_load_model_menu_fun, title="Back")
        ]


def load_knight(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.append('n')

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -5), go_to_load_model_menu_fun, title="Back")
    ]


def load_bishop(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.append('b')

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -5), go_to_load_model_menu_fun, title="Back")
    ]


def load_rook(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.append('r')

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -5), go_to_load_model_menu_fun, title="Back")
    ]


def load_pawn(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.append('p')

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -5), go_to_load_model_menu_fun, title="Back")
    ]



def set_figure_buttons(render):
    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 12), load_king, title="King"),
        bu.Button(Vector2d(0, 8), load_queen, title="Queen"),
        bu.Button(Vector2d(0, 4), load_rook, title="Rook"),
        bu.Button(Vector2d(0, 0), load_knight, title="Knight"),
        bu.Button(Vector2d(0, -4), load_bishop, title="Bishop"),
        bu.Button(Vector2d(0, -8), load_pawn, title="Pawn"),

        bu.Button(Vector2d(0, -13), go_to_load_model_menu_fun, title="Back")
    ]

def load_white_figures_menu(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)
    render.room.user_param.append("white")
    set_figure_buttons(render)

def load_black_figures_menu(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)
    render.room.user_param.append("black")
    set_figure_buttons(render)


def load_board(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 0), render.room.process_data, title="OK"),
        bu.Button(Vector2d(0, -5), go_to_load_model_menu_fun, title="Back")
                                ]

    render.room.text_fields_prim = [tf.TextField(Vector2d(0, 5), title="Path to .png")]


def go_to_load_model_menu_fun(render):
    render.state = om.RenderState.MENU
    of.clear_fun(render)

    render.room.user_param.clear()

    render.room.buttons_prim = [
        bu.Button(Vector2d(0, 10), load_white_figures_menu, title="White figures"),
        bu.Button(Vector2d(0, 5), load_black_figures_menu, title="Black figures"),
        bu.Button(Vector2d(0, 0), load_board, title="Board"),
        bu.Button(Vector2d(0, -5), of.main_menu, title="Back")
                                ]
    render.room.text_fields_prim = None