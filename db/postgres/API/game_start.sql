CREATE OR REPLACE PROCEDURE chess.game_start(
	p_user_id1 integer,
	p_user_id2 integer,
	p_game_time TIME,
	p_adding_time integer,
	p_user1_side bit,
	p_user2_side bit)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
  v_user_id1_by_side integer;
  v_user_id2_by_side integer;
  v_users_swap_flag bit;
  v_rate_coef float;
  v_game_id bigint;
  v_user1 chess.players%rowtype;
  v_user2 chess.players%rowtype;
BEGIN
----LOCK TABLE ONLY chess.game;

SELECT 0::BIT into v_users_swap_flag;
-- calculate game sides
IF p_user1_side ISNULL THEN
    IF p_user2_side NOTNULL THEN
	    IF p_user2_side = 0 THEN
            SELECT 1::BIT INTO v_users_swap_flag;
		END IF;
    END IF;
ELSE
    SELECT p_user1_side::BIT INTO v_users_swap_flag;
END IF;

IF v_users_swap_flag = 1::BIT THEN
    SELECT p_user_id2 INTO v_user_id1_by_side;
    SELECT p_user_id1 INTO v_user_id2_by_side;
ELSE
    SELECT p_user_id1 INTO v_user_id1_by_side;
    SELECT p_user_id2 INTO v_user_id2_by_side;
END IF;

SELECT * into v_user1 FROM chess.players WHERE chess.players.user_id = v_user_id1_by_side;
SELECT * into v_user2 FROM chess.players WHERE chess.players.user_id = v_user_id2_by_side;

SELECT 1 / (1 + power(10, CAST(ABS(v_user1.rate - v_user1.rate) AS INTEGER) /
                                   400.0)) INTO v_rate_coef;

INSERT INTO chess.game (user_id1, user_id2, win_cost, draw_cost,
                        adding_time, player1_time_left,
                        player2_time_left, player1_pack, player2_pack) VALUES
                        (v_user_id1_by_side, v_user_id2_by_side, CAST(v_rate_coef AS integer),
                         CAST(v_rate_coef / 2 AS integer), p_adding_time,
                         p_game_time, p_game_time,
                         v_user1.current_pack, v_user2.current_pack) RETURNING game_id into v_game_id;

begin
    call chess.add_game_message(p_game_id := v_game_id, p_add_user1 :=  1::bit, p_add_user2 := 1::bit);
end;
END;

$BODY$;