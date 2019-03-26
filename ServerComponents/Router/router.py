import ServerComponents.Controllers.ChessGameController.game_controller as game_controller
import ServerComponents.Controllers.ChessUsersController.users_controller as users_controller
import pyodbc

"""
class for route messages to controller function on server
"""
class router:
    def __init__(self):
        self.actions = \
            {
                # game
                'game_stop': game_controller.game_stop, 'start_find_game': game_controller.start_find_game,
                'stop_find_game': game_controller.stop_find_game, 'update_board': game_controller.update_board,
                # users
                'login': users_controller.login, 'auth': users_controller.auth,
                'auth_confirm': users_controller.auth_confirm
            }

        None

    def run(self, msg):
        #parse msg to action_name and action_params

        #self.actions[action](params)

        None