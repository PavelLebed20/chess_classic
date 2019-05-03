create function login(p_user_login_or_mail character varying, p_user_password character varying) returns integer
    language plpgsql
as
$$
DECLARE
    v_user_id int;
    v_user1_id int;
    v_user2_id int;
    v_game_id bigint;
    v_login_data varchar;
    v_user1_data varchar;
    v_user2_data varchar;
    v_game_board varchar(64);
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
          chess.game.user_id1 = v_user_id and chess.game.is_playing = 1::bit
      LIMIT 1;
      if v_game_id IS NOT NULL then
          call chess.a
      end if;

    begin
	  call chess.add_message(p_data := v_login_data, p_user_id := v_user_id, p_action_name := 'login');
    end;
    return v_user_id;
  end;
  end if;
  return -1;
END;

$$;

alter function login(varchar, varchar) owner to postgres;

