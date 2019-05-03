CREATE OR REPLACE PROCEDURE chess.add_game_message(
	p_game_id bigint,
    p_add_user1 BIT,
    p_add_user2 BIT )
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_game_row chess.game%ROWTYPE;
    v_user1_info chess.players%ROWTYPE;
    v_user2_info chess.players%ROWTYPE;
    v_user_data varchar;
BEGIN
    SELECT * INTO v_game_row FROM chess.game WHERE chess.game.game_id = p_game_id;
    SELECT * INTO v_user2_info FROM chess.players WHERE chess.players.user_id = v_game_row.user_id2;
    SELECT * INTO v_user1_info FROM chess.players WHERE chess.players.user_id = v_game_row.user_id1;
    if p_add_user1 = 1::bit then
        begin
            SELECT CONCAT('update_game?board=', v_game_row.board,
                          '&opponent_login=', v_user2_info.login,
                          '&opponent_rate=', v_user2_info.rate,
                          '&self_time=' , v_game_row.player1_time_left,
                          '&opponent_time=', v_game_row.player2_time_left,
                          '&is_playing=' ,  v_game_row.is_playing,
                          '&self_rate=', v_user1_info.rate,
                          '&result=', v_game_row.game_result,
                          '&side=0',
                          '&next_move=', v_game_row.next_move_player) INTO v_user_data;

                begin
	                call chess.add_message(p_data := v_user_data, p_user_id := v_game_row.user_id1,
	                                       p_action_name := 'update_game');
                end;
        end;
    end if;
    if p_add_user2 = 1::bit then
        begin
            SELECT CONCAT('update_game?board=', v_game_row.board,
                          '&opponent_login=', v_user1_info.login,
                          '&opponent_rate=', v_user1_info.rate,
                          '&self_time=' , v_game_row.player2_time_left,
                          '&opponent_time=', v_game_row.player1_time_left,
                          '&is_playing=' ,  v_game_row.is_playing,
                          '&self_rate=', v_user2_info.rate,
                          '&result=', v_game_row.game_result,
                          '&side=1',
                          '&next_move=', v_game_row.next_move_player) INTO v_user_data;

                begin
	                call chess.add_message(p_data := v_user_data, p_user_id := v_game_row.user_id2,
	                                       p_action_name := 'update_game');
                end;
        end;
    end if;
end;

$BODY$