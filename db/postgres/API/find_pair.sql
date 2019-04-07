CREATE OR REPLACE PROCEDURE chess.find_pair(
	user_id integer,
	low_rate integer,
	high_rate integer,
	adding_time integer,
	game_time TIME,
	side bit DEFAULT NULL)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  pairing_id bigint;
  total_rows integer;
BEGIN

IF EXISTS (SELECT 1 FROM chess.game WHERE
           chess.game.user_id1 = user_id or chess.game.user_id2 = user_id and is_playing = True) THEN
           RETURN;
END IF;


LOCK TABLE ONLY chess.pairing;

UPDATE chess.pairing SET chess.pairing.low_rate = low_rate, chess.pairing.high_rate = high_rate WHERE
chess.pairing.user_id = user_id and chess.pairing.game_time = game_time and chess.pairing.adding_time = adding_time;
GET DIAGNOSTICS total_rows := ROW_COUNT;
IF total_rows > 0 THEN
    COMMIT;
    RETURN;
END IF;

CREATE TEMP TABLE pairing_table_tmp
(
   BIGINT pairing_id
);
INSERT INTO pairing_table_tmp (SELECT pairing_id FROM chess.pairing
                               JOIN chess.players ON chess.pairing.user_id = chess.players.user_id
                               WHERE chess.pairing.game_time = game_time and
                               chess.pairing.adding_time = adding_time and
                               chess.players.rate between low_rate - 1 and high_rate and
							                 (side ISNULL or chess.pairing.side ISNULL or chess.pairing.side != side)
							   ORDER BY chess.pairing.game_time LIMIT 1);

IF EXISTS (SELECT 1 FROM pairing_table_tmp) THEN
   SELECT pairing_id FROM pairing_table_tmp INTO pairing_id;
   DELETE FROM chess.pairing WHERE chess.pairing.pairing_id = pairing_id;
   -- run game start
ELSE
   INSERT INTO chess.pairing (user_id, low_rate, high_rate, adding_time, game_time) VALUES
   (user_id, low_rate, high_rate, adding_time, game_time);
END IF;

DROP TABLE pairing_table_tmp;

COMMIT;
END;
$BODY$;
