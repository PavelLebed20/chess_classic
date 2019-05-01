CREATE EXTENSION IF NOT EXISTS pgcrypto;

create or replace function chess.registrate(
p_login varchar(50),
p_password varchar(64),
p_rate int,
p_email varchar(50),
p_auth_length integer default 64) returns varchar as
$$
declare
  v_user_id int;
  v_auth_code varchar;
BEGIN
  IF p_login IS NULL THEN
    RETURN NULL;
  end if;

  IF p_password THEN
    RETURN NULL;
  end if;

  IF p_rate IS NULL OR p_rate <= 0 OR p_rate >= 5000 THEN
    RETURN NULL;
  end if;

  IF p_email IS NULL THEN
    RETURN NULL;
  end if;

  SELECT chess.players.user_id into v_user_id FROM chess.players WHERE chess.players.login = p_login or
                                                       chess.players.email = p_email LIMIT 1;
  if v_user_id notnull then
    RETURN NULL;
  end if;
  select chess.random_string(length := p_auth_length) into v_auth_code;

  begin
    LOCK TABLE only chess.players;
    LOCK TABLE only chess.auth_codes;

    INSERT into chess.players (login, password_salt, rate, email) VALUES
    (p_login, crypt(p_password, gen_salt('bf')), p_rate, p_email)
    RETURNING chess.user_id INTO v_user_id;

    INSERT INTO chess.auth_codes (user_id, code_salt) VALUES
    (v_user_id, crypt(v_auth_code, gen_salt('bf')));
  end;
  RETURN v_auth_code;
end;
$$ LANGUAGE plpgsql;