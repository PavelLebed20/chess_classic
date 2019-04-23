CREATE OR REPLACE FUNCTION chess.get_current_game_board(
p_user_id integer) RETURNS varchar AS $$

DECLARE
 v_board varchar;
BEGIN

SELECT cast(chess.game.board as varchar) into v_board FROM chess.game WHERE (chess.game.user_id1 = p_user_id or chess.game.user_id2 = p_user_id) and
                                                                                chess.game.is_playing = 1::BIT LIMIT 1;
return v_board;
END;
$$ LANGUAGE 'plpgsql';