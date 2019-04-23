CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE OR REPLACE function chess.login(
	p_user_login_or_mail varchar,
	p_user_password varchar)
	RETURNS INTEGER AS $$

DECLARE
    v_user_id int;
    v_user1_id int;
    v_user2_id int;
    v_game_id bigint;
    v_login_data varchar;
    v_user1_data varchar;
    v_user2_data varchar;
    v_game_board bytea;
BEGIN
  SELECT chess.players.user_id into v_user_id FROM chess.players WHERE chess.players.login = p_user_login_or_mail or
                                                       chess.players.email = p_user_login_or_mail and
                                                       chess.players.password_salt = crypt(p_user_password,
                                                                                     chess.players.password_salt);
  if v_user_id notnull then
    SELECT CONCAT('login?self_rate=', (select cast(chess.players.rate as varchar) FROM chess.players
      where chess.players.user_id=v_user_id), '&self_id=', v_user_id) into v_login_data;

    begin
      UPDATE chess.players SET online = 1::bit WHERE user_id = v_user_id;

      LOCK TABLE ONLY chess.messages in share mode;

      SELECT chess.game.game_id INTO v_game_id FROM chess.game WHERE
          (chess.game.user_id1 = v_user_id OR chess.game.user_id2 = v_user_id) and chess.game.is_playing = 1::bit
      LIMIT 1;

      if (v_game_id is not null) then


            SELECT chess.game.user_id1 INTO v_user1_id from chess.game where chess.game.game_id = v_game_id limit 1;

            SELECT chess.game.user_id2 INTO v_user2_id from chess.game where chess.game.game_id = v_game_id limit 1;

            SELECT CONCAT('update_game?',
                'opponent_login=', (select cast(chess.players.login as varchar) FROM chess.players WHERE
                                                 chess.players.user_id=v_user2_id LIMIT 1) ,
             '&opponent_rate=' , (select cast(chess.players.rate as varchar)
                            FROM chess.players WHERE chess.players.user_id=v_user2_id LIMIT 1) ,
             '&self_time=' , (select cast(chess.game.player1_time_left as varchar)
                              FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&opponent_time=' , (select cast(chess.game.player2_time_left as varchar)
                                  FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1) ,
             '&is_over=' ,  (select case when chess.game.is_playing = 1::bit then cast(0::bit as varchar)
                             else cast(1::bit as varchar) end
                             FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&self_rate=', (select cast(chess.players.rate as varchar) FROM chess.players WHERE
                                         chess.players.user_id=v_user1_id LIMIT 1),
             '&result=', (select cast(chess.game.game_result as varchar) FROM chess.game WHERE
                                         chess.game.game_id=v_game_id LIMIT 1) ,
             '&side=0',
             '&next_move=', (select cast(chess.game.next_move_player as varchar) FROM chess.game WHERE
                                         chess.game.game_id=v_game_id LIMIT 1)) INTO v_user1_data;

  SELECT CONCAT('update_game?',
                'opponent_login=', (select cast(chess.players.login as varchar) FROM chess.players WHERE
                                                 chess.players.user_id=v_user1_id LIMIT 1) ,
             '&opponent_rate=' , (select cast(chess.players.rate as varchar)
                            FROM chess.players WHERE chess.players.user_id=v_user1_id LIMIT 1) ,
             '&self_time=' , (select cast(chess.game.player2_time_left as varchar)
                              FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&opponent_time=' , (select cast(chess.game.player1_time_left as varchar)
                                  FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1) ,
             '&is_over=' ,  (select case when chess.game.is_playing = 1::bit then cast(0::bit as varchar)
                             else cast(1::bit as varchar) end
                             FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1),
             '&self_rate=', (select cast(chess.players.rate as varchar) FROM chess.players WHERE
                                         chess.players.user_id=v_user2_id LIMIT 1),
             '&result=', (select cast(chess.game.game_result as varchar) FROM chess.game WHERE
                                         chess.game.game_id=v_game_id LIMIT 1),
             '&side=1',
             '&next_move=', (select cast(chess.game.next_move_player as varchar) FROM chess.game WHERE
                                         chess.game.game_id=v_game_id LIMIT 1)) INTO v_user2_data;

  select chess.game.board into v_game_board FROM chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;

  begin
	call chess.add_message(p_data := v_user1_data, p_user_id := v_user1_id, p_action_name := 'update_game',
	    p_byte_data := v_game_board);
  end;
  begin
	call chess.add_message(p_data := v_user2_data, p_user_id := v_user2_id, p_action_name := 'update_game',
	    p_byte_data := v_game_board);
  end;
      end if;
    begin
	  call chess.add_message(p_data := v_login_data, p_user_id := v_user_id, p_action_name := 'login');
    end;
    return v_user_id;
  end;
  end if;
  return -1;
END;

$$ LANGUAGE plpgsql;;