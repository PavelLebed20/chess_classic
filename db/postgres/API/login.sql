CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE OR REPLACE function chess.login(
	p_user_login_or_mail varchar,
	p_user_password varchar)
	RETURNS INTEGER AS $$

DECLARE
    v_user chess.players%ROWTYPE;
    v_login_data varchar;
BEGIN
  SELECT * into v_user FROM chess.players WHERE (chess.players.login = p_user_login_or_mail or
                                                       chess.players.email = p_user_login_or_mail) and
                                                       chess.players.password_salt = crypt(p_user_password,
                                                                                     chess.players.password_salt)
                                                      ;-- and chess.players.online = 0::bit;
  if v_user notnull then
    begin
        UPDATE chess.players SET online = 1::bit WHERE user_id = v_user.user_id;
    end;
    if v_user.verified = 0::bit then
        begin
	        call chess.add_message(p_data := 'login?not_verified=1',
	            p_user_id := v_user.user_id, p_action_name := 'login');
        end;
    else
        SELECT CONCAT('login?self_rate=', v_user.rate, '&self_id=', v_user.user_id) into v_login_data;
        begin
            call chess.add_message(p_data := v_login_data, p_user_id := v_user.user_id, p_action_name := 'login');
        end;
        begin
            call chess.add_game_message_if_exists(v_user.user_id);
        end;
    end if;
    return v_user.user_id;
  end if;
  return -1;
END;

$$ LANGUAGE plpgsql;
