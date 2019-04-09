CREATE OR REPLACE PROCEDURE chess.update_game_state(
	p_user_id integer,
	p_left_time TIME,
	p_board bytea,
	p_is_playing bit DEFAULT 1::bit,
	p_game_result bit DEFAULT NULL)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  v_game_id integer;
BEGIN
  SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id1 = p_user_id and
                                                                 chess.game.is_playing = 1::bit;
  if v_game_id notnull then
      LOCK TABLE ONLY chess.game;
      update chess.game set player1_time_left = p_left_time, board = p_board, is_playing = p_is_playing,
                            game_result = p_game_result where chess.game.game_id=v_game_id;
  else
      SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id2 = p_user_id and
                                                                     chess.game.is_playing = 1::bit;
      LOCK TABLE ONLY chess.game;
      update chess.game set player2_time_left = p_left_time, board = p_board, is_playing = p_is_playing,
                            game_result = p_game_result where chess.game.game_id=v_game_id;
  end if;

  -- obtain rate
  if p_is_playing = 0::bit then
      LOCK TABLE ONLY chess.players;
      update chess.players set rate = case
                                        when p_game_result isnull then rate + (SELECT chess.game.draw_cost FROM
                                                                                 chess.game WHERE
                                                                                 chess.game.game_id=v_game_id)
                                        when p_game_result = 0::bit then rate +
                                                                                (SELECT chess.game.win_cost FROM
                                                                                 chess.game WHERE
                                                                                 chess.game.game_id=v_game_id)
                                        else rate - (SELECT chess.game.win_cost FROM
                                                            chess.game WHERE
                                                            chess.game.game_id=v_game_id)
                                      end
      WHERE user_id = (SELECT chess.game.user_id1 FROM chess.game WHERE chess.game.game_id=v_game_id);

      update chess.players set rate = case
                                        when p_game_result isnull then rate - (SELECT chess.game.draw_cost FROM
                                                                                 chess.game WHERE
                                                                                 chess.game.game_id=v_game_id)
                                        when p_game_result = 0::bit then rate -
                                                                                (SELECT chess.game.win_cost FROM
                                                                                 chess.game WHERE
                                                                                 chess.game.game_id=v_game_id)
                                        else rate + (SELECT chess.game.win_cost FROM
                                                            chess.game WHERE
                                                            chess.game.game_id=v_game_id)
                                      end
      WHERE user_id = (SELECT chess.game.user_id2 FROM chess.game WHERE chess.game.game_id=v_game_id);
  end if;
END;

$BODY$;