CREATE OR REPLACE PROCEDURE chess.update_game_state(
	p_user_id integer,
	p_board varchar(64),
	p_is_playing bit DEFAULT 1::bit,
	p_game_result bit DEFAULT NULL)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  v_user1_id integer;
  v_user2_id integer;
  v_game_id integer;
  v_date_diff bigint;
  v_left_time TIME;
  v_last_update timestamp;
  v_add_time int;
BEGIN
  SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id1 = p_user_id and
                                                                 chess.game.is_playing = 1::bit LIMIT 1;
  if v_game_id notnull then
      SELECT chess.game.last_update INTO v_last_update from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
      SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), v_last_update) INTO v_date_diff;
      SELECT chess.game.player1_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
      SELECT v_left_time - make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_left_time;
      if v_left_time > TIME '00:00:00' then
          SELECT chess.game.adding_time INTO v_add_time FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
          SELECT v_left_time + make_interval(secs := CAST(v_add_time AS double precision)) INTO v_left_time;
      end if;

      LOCK TABLE ONLY chess.game in share row exclusive mode;
      update chess.game set player1_time_left = v_left_time, board = p_board, is_playing = p_is_playing,
                            game_result = p_game_result, next_move_player =
                                case when next_move_player = 0::bit then 1::bit else 0::bit end,
                            last_update = NOW()
                            where chess.game.game_id=v_game_id;

      select chess.game.user_id1 into v_user1_id FROM chess.game where chess.game.game_id=v_game_id LIMIT 1;
      select chess.game.user_id2 into v_user2_id FROM chess.game where chess.game.game_id=v_game_id LIMIT 1;
  else
      SELECT chess.game.game_id into v_game_id FROM chess.game WHERE chess.game.user_id2 = p_user_id and
                                                                     chess.game.is_playing = 1::bit LIMIT 1;

      SELECT chess.game.last_update INTO v_last_update from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
      SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), v_last_update) INTO v_date_diff;
      SELECT chess.game.player2_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
      SELECT v_left_time - make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_left_time;
      if v_left_time > TIME '00:00:00' then
          SELECT chess.game.adding_time INTO v_add_time FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
          SELECT v_left_time + make_interval(secs := CAST(v_add_time AS double precision)) INTO v_left_time;
      end if;

      LOCK TABLE ONLY chess.game in share row exclusive mode;
      update chess.game set player2_time_left = v_left_time, board = p_board, is_playing = p_is_playing,
                            game_result = p_game_result, next_move_player =
                                case when next_move_player = 0::bit then 1::bit else 0::bit end,
                            last_update = NOW()
                            where chess.game.game_id=v_game_id;


      select chess.game.user_id1 into v_user1_id FROM chess.game where chess.game.game_id=v_game_id LIMIT 1;
      select chess.game.user_id2 into v_user2_id FROM chess.game where chess.game.game_id=v_game_id LIMIT 1;
  end if;

  -- obtain rate
  if p_is_playing = 0::bit then
      --LOCK TABLE ONLY chess.players;
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

  begin
      call chess.add_game_message(p_game_id := v_game_id, p_add_user1 := 1::bit, p_add_user2 := 1::bit);
  end;

END;

$BODY$;