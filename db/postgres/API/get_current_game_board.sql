CREATE OR REPLACE PROCEDURE chess.get_current_game_board(
p_user_id integer)
LANGUAGE 'plpgsql'

AS $BODY$
BEGIN
SELECT chess.game.board FROM chess.game WHERE chess.game.user_id1 = p_user_id or chess.game.user_id2 = p_user_id and
                                                                                 chess.game.is_playing = 1::BIT;
END;
$BODY$;