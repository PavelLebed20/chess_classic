CREATE OR REPLACE FUNCTION chess.get_emails() RETURNS
    table(email varchar(128), login varchar(128), auth_code varchar(64)) AS $$
DECLARE
begin
    CREATE temporary table IF NOT EXISTS temp_players_user_ids
    AS  SELECT chess.players.user_id
        from chess.players JOIN chess.auth_codes ON players.user_id = auth_codes.user_id
        WHERE chess.players.verified = 0::bit and chess.auth_codes.send = 0::bit;

        UPDATE chess.auth_codes SET send = 1::bit WHERE chess.auth_codes.user_id in
         (select * from temp_players_user_ids);

        RETURN QUERY SELECT chess.players.email, chess.players.login,
                            chess.auth_codes.auth_code
        from chess.players JOIN chess.auth_codes ON players.user_id = auth_codes.user_id
        WHERE chess.players.user_id in (select * from temp_players_user_ids);

END;

$$ LANGUAGE 'plpgsql';