CREATE OR REPLACE PROCEDURE chess.update_game_state(
	p_user_id integer,
	p_left_time TIME,
	p_board bytea,
	p_is_playing bit DEFAULT 1::bit,
	p_game_result bit DEFAULT NULL)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  v_user1_id integer;
  v_user2_id integer;
  v_game_id integer;
  v_user1_data varchar;
  v_user2_data varchar;
BEGIN
  SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id1 = p_user_id and
                                                                 chess.game.is_playing = 1::bit LIMIT 1;
  if v_game_id notnull then
      LOCK TABLE ONLY chess.game;
      update chess.game set player1_time_left = p_left_time, board = p_board, is_playing = p_is_playing,
                            game_result = p_game_result where chess.game.game_id=v_game_id;

      select chess.game.user_id1 into v_user1_id where chess.game.game_id=v_game_id LIMIT 1;
      select chess.game.user_id2 into v_user2_id where chess.game.game_id=v_game_id LIMIT 1;
  else
      SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id2 = p_user_id and
                                                                     chess.game.is_playing = 1::bit LIMIT 1;
      LOCK TABLE ONLY chess.game;
      update chess.game set player2_time_left = p_left_time, board = p_board, is_playing = p_is_playing,
                            game_result = p_game_result where chess.game.game_id=v_game_id;


      select chess.game.user_id2 into v_user1_id where chess.game.game_id=v_game_id LIMIT 1;
      select chess.game.user_id1 into v_user2_id where chess.game.game_id=v_game_id LIMIT 1;
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

  SELECT CONCAT('update_game?&board=', (select cast(chess.game.board as varchar)
                                        FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1) ,
                '&opponent_login=', (select cast(chess.players.login as varchar) FROM chess.players WHERE
                                                 chess.players.user_id=v_user2_id LIMIT 1) ,
             '&opponent_rate=' , (select cast(chess.players.rate as varchar)
                            FROM chess.players WHERE chess.players.user_id=v_user2_id LIMIT 1) ,
             '&self_time=' , (select cast(chess.game.player1_time_left as varchar)
                              FROM chess.players WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&opponent_time=' , (select cast(chess.game.player2_time_left as varchar)
                                  FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1) ,
             '&is_over=' ,  (select case when chess.game.is_playing = 1::bit then cast(0::bit as varchar)
                             else cast(0::bit as varchar) end
                             FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&self_rate=', (select cast(chess.players.rate as varchar) FROM chess.players WHERE
                                         chess.players.user_id=v_user1_id LIMIT 1),
             '&result=', (select cast(chess.game.game_result as varchar) FROM chess.game WHERE
                                         chess.game.game_id=v_game_id LIMIT 1)) INTO v_user1_data;

  SELECT CONCAT('update_game?&board=', (select cast(chess.game.board as varchar)
                                        FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1) ,
                '&opponent_login=', (select cast(chess.players.login as varchar) FROM chess.players WHERE
                                                 chess.players.user_id=v_user1_id LIMIT 1) ,
             '&opponent_rate=' , (select cast(chess.players.rate as varchar)
                            FROM chess.players WHERE chess.players.user_id=v_user1_id LIMIT 1) ,
             '&self_time=' , (select cast(chess.game.player2_time_left as varchar)
                              FROM chess.players WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&opponent_time=' , (select cast(chess.game.player1_time_left as varchar)
                                  FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1) ,
             '&is_over=' ,  (select case when chess.game.is_playing = 1::bit then cast(0::bit as varchar)
                             else cast(0::bit as varchar) end
                             FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&self_rate=', (select cast(chess.players.rate as varchar) FROM chess.players WHERE
                                         chess.players.user_id=v_user2_id LIMIT 1),
             '&result=', (select cast(chess.game.game_result as varchar) FROM chess.game WHERE
                                         chess.game.game_id=v_game_id LIMIT 1)) INTO v_user2_data;

  begin
	call chess.add_message(p_data := v_user1_data, p_user_id := v_user1_id, p_action_name := 'update_game');
  end;
  begin
	call chess.add_message(p_data := v_user2_data, p_user_id := v_user2_id, p_action_name := 'update_game');
  end;

END;

$BODY$;