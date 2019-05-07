CREATE OR REPLACE function chess.check_game_update_params(
	p_user_id integer,
	p_left_time TIME)
	RETURNS boolean AS $$

DECLARE
    v_game_id bigint;
    v_next_player bit;
    v_left_time TIME;
BEGIN
  SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id1 = p_user_id and
                                                               chess.game.is_playing = 1::bit;

  IF v_game_id NOTNULL THEN
       SELECT 0::bit into v_next_player;
       select chess.game.player1_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
  else
      SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id2 = p_user_id and
                                                               chess.game.is_playing = 1::bit;
      IF v_game_id NOTNULL THEN
        SELECT 1::bit into v_next_player;
        select chess.game.player2_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
      else
          return FALSE;
      END IF;
  end if;

  if (select chess.game.next_move_player FROM chess.game WHERE chess.game.game_id=v_game_id) != v_next_player THEN
      RETURN FALSE;
  end if;

  if (v_left_time - p_left_time) >=
     (SELECT  TO_CHAR((chess.game.adding_time || ' second')::interval, 'HH24:MI:SS')
      FROM chess.game WHERE chess.game.game_id=v_game_id) THEN
      RETURN FALSE;
  end if;
  RETURN TRUE;
END;

$$ LANGUAGE plpgsql;;