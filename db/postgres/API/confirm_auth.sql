CREATE OR REPLACE PROCEDURE chess.confirm_auth(
	p_email varchar(128),
	p_auth_code varchar(64))
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_user_id integer;
BEGIN
    SELECT chess.auth_codes.user_id FROM chess.auth_codes
     JOIN chess.players ON chess.auth_codes.user_id = chess.players.user_id
     where chess.players.email = p_email and chess.auth_codes.auth_code = p_auth_code
     limit 1
     into v_user_id;
     if v_user_id isnull then
         return;
     end if;
    UPDATE chess.players SET verified = 1::bit WHERE chess.players.user_id = v_user_id;
    UPDATE chess.auth_codes SET send = 1::bit WHERE chess.auth_codes.send = 1::bit;
end;

$BODY$