CREATE OR REPLACE PROCEDURE chess.find_pair(
	p_user_id integer,
	p_low_rate integer,
	p_high_rate integer,
	p_adding_time integer,
	p_game_time TIME,
	p_side bit DEFAULT NULL)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  v_pairing_id bigint;
  v_opponent_id integer;
  v_opponent_side bit;
BEGIN

IF EXISTS (SELECT 1 FROM chess.game WHERE
           (chess.game.user_id1 = p_user_id or chess.game.user_id2 = p_user_id) and chess.game.is_playing = 1::BIT) THEN
           RETURN;
END IF;

DELETE FROM chess.pairing WHERE chess.pairing.user_id = p_user_id;
begin
LOCK TABLE ONLY chess.pairing;

SELECT chess.pairing.pairing_id INTO v_pairing_id FROM chess.pairing
                                JOIN chess.players ON chess.pairing.user_id = chess.players.user_id
                                WHERE chess.pairing.game_time = p_game_time and
                                chess.pairing.user_id != p_user_id and
                                chess.pairing.adding_time = p_adding_time and
                                chess.players.rate between p_low_rate - 1 and p_high_rate and
							                 (p_side ISNULL or chess.pairing.side ISNULL or
							                  chess.pairing.side != p_side)
							    ORDER BY chess.pairing.game_time LIMIT 1;

IF v_pairing_id NOTNULL THEN
   SELECT chess.pairing.user_id INTO v_opponent_id FROM chess.pairing WHERE chess.pairing.pairing_id = v_pairing_id;
   SELECT chess.pairing.side INTO v_opponent_side FROM chess.pairing WHERE chess.pairing.pairing_id = v_pairing_id;

   DELETE FROM chess.pairing WHERE chess.pairing.pairing_id = v_pairing_id;
   -- run game start
   begin
	call chess.game_start(
		p_user_id1 := p_user_id,
		p_user_id2 := v_opponent_id,
		p_game_time := p_game_time,
		p_adding_time := p_adding_time,
		p_user1_side := p_side,
		p_user2_side := v_opponent_side);
    end;
ELSE
   INSERT INTO chess.pairing (user_id, low_rate, high_rate, adding_time, game_time) VALUES
   (p_user_id, p_low_rate, p_high_rate, p_adding_time, p_game_time);
END IF;
end;
END;
$BODY$;
