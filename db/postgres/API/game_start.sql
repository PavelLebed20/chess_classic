CREATE OR REPLACE PROCEDURE chess.game_start(
	user_id1 integer,
	user_id2 integer,
	game_time TIME,
	adding_time integer,
	user1_side bit, -- (0 - white, 1 - black, NULL - any)
	user2_side bit) -- (0 - white, 1 - black, NULL - any)
	LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  user_id1_by_side integer;
  user_id2_by_side integer;
  users_swap_flag bit;
  delta_rate integer;
  user1_rate integer;
  user2_rate integer;
  rate_coef float;
BEGIN

LOCK TABLE ONLY chess.game;

SET users_swap_flag = 0;
-- calculate game sides
IF user1_side ISNULL THEN
    IF user2_side NOTNULL THEN
	    IF user2_side = 0 THEN
            SET users_swap_flag = 1;
	    ELSE
		    SET users_swap_flag = 0;
		  END IF;
    END IF;
ELSE
    SET users_swap_flag = user1_side;
END IF;

IF users_swap_flag != 0 THEN
    user_id1_by_side = user_id2;
    user_id2_by_side = user_id1;
ELSE
    user_id1_by_side = user_id1;
    user_id2_by_side = user_id2;
END IF;

SELECT chess.players.rate FROM chess.players INTO user1_rate WHERE user_id = user_id1;
SELECT chess.players.rate FROM chess.players INTO user2_rate WHERE user_id = user_id2;
SELECT CAST(ABS(user_id1 - user_id2) AS INTEGER) INTO delta_rate;
SELECT 1 / (1 + power(10, delta_rate / 400)) INTO rate_coef;

INSERT INTO chess.game (user_id1_by_side, user_id2_by_side, win_cost, draw_cost,
                        adding_time, player1_time_left,
                        player2_time_left) VALUES
                        (user_id1_by_side, user_id2_by_side, CAST(rate_coef AS integer),
                         CAST(rate_coef / 2 AS integer), adding_time,
                         game_time, game_time);

INSERT INTO chess.messages(data, user_id, message_type_id, priority) VALUES
     ("", user_id1_by_side, 1, 1), ("", user_id2_by_side, 1, 1);

COMMIT;
END;

$BODY$;