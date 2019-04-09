CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE OR REPLACE function chess.login(
	p_user_login_or_mail varchar,
	p_user_password varchar)
	RETURNS INTEGER AS $$

DECLARE
    v_user_id int;
    v_login_data varchar;
BEGIN
  SELECT chess.players.user_id into v_user_id FROM chess.players WHERE chess.players.login = p_user_login_or_mail or
                                                       chess.players.email = p_user_login_or_mail and
                                                       chess.players.password_salt = crypt(p_user_password,
                                                                                     chess.players.password_salt);
  if v_user_id notnull then
    SELECT CONCAT('login?self_rate=', (select cast(chess.players.rate as varchar) FROM chess.players
      where chess.players.user_id=v_user_id)) into v_login_data;

    begin
	  call chess.add_message(p_data := v_login_data, p_user_id := v_user_id, p_action_name := 'login');
    end;
    return v_user_id;
  end if;
  return -1;
END;

$$ LANGUAGE plpgsql;;