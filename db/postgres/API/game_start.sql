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
  v_user1_data varchar;
  v_user2_data varchar;
BEGIN
LOCK TABLE ONLY chess.game;

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

SELECT 1 / (1 + power(10, CAST(ABS((SELECT chess.players.rate FROM chess.players
                                    WHERE chess.players.user_id = p_user_id1) -
                                   (SELECT chess.players.rate FROM chess.players
                                    WHERE chess.players.user_id = p_user_id2)) AS INTEGER) /
                                   400.0)) INTO v_rate_coef;

INSERT INTO chess.game (user_id1, user_id2, win_cost, draw_cost,
                        adding_time, player1_time_left,
                        player2_time_left) VALUES
                        (v_user_id1_by_side, v_user_id2_by_side, CAST(v_rate_coef AS integer),
                         CAST(v_rate_coef / 2 AS integer), p_adding_time,
                         p_game_time, p_game_time);

SELECT CONCAT('update_game?&board=', '&opponent_login=',
	    (select cast(chess.players.login as varchar) FROM chess.players WHERE
                                                         chess.players.user_id=v_user_id2_by_side LIMIT 1) ,
             '&opponent_rate=' , (select cast(chess.players.rate as varchar)
                            FROM chess.players WHERE chess.players.user_id=v_user_id2_by_side LIMIT 1) ,
             '&self_time=' , cast(p_game_time as varchar) , '&opponent_time=' , cast(p_game_time as varchar) ,
             '&is_over=0' , '&self_rate=&result=') INTO v_user1_data;

SELECT  CONCAT('update_game?&board=', '&opponent_login=',
	    (select cast(chess.players.login as varchar) FROM chess.players WHERE
                                                         chess.players.user_id=v_user_id1_by_side LIMIT 1) ,
             '&opponent_rate=' , (select cast(chess.players.rate as varchar)
                            FROM chess.players WHERE chess.players.user_id=v_user_id1_by_side LIMIT 1) ,
             '&self_time=' , cast(p_game_time as varchar) , '&opponent_time=' , cast(p_game_time as varchar) ,
             '&is_over=0' , '&self_rate==&result=') INTO v_user2_data;

begin
	call chess.add_message(p_data := v_user1_data, p_user_id := v_user_id1_by_side, p_action_name := 'update_game');
end;
begin
	call chess.add_message(p_data := v_user2_data, p_user_id := v_user_id2_by_side, p_action_name := 'update_game');
end;
END;

$BODY$;