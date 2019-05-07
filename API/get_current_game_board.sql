CREATE OR REPLACE FUNCTION chess.get_current_game_board_state(
p_user_id integer) RETURNS table(board varchar, side bit) AS $$

DECLARE
BEGIN

RETURN QUERY SELECT cast(chess.game.board as varchar), chess.game.next_move_player
                    FROM chess.game WHERE
                    (chess.game.user_id1 = p_user_id or chess.game.user_id2 = p_user_id) and
                     chess.game.is_playing = 1::BIT LIMIT 1;
END;
$$ LANGUAGE 'plpgsql';