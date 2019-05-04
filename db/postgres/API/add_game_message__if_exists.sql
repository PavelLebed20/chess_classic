CREATE OR REPLACE PROCEDURE chess.add_game_message_if_exists(
	p_user_id int)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_game_id bigint;
    v_date_diff bigint;
    v_left_time TIME;
    v_last_update timestamp;
    v_next_move bit;
    v_add_time int;
BEGIN
   LOCK TABLE ONLY chess.messages in share mode;

    SELECT chess.game.game_id INTO v_game_id FROM chess.game WHERE
          chess.game.user_id1 = p_user_id and chess.game.is_playing = 1::bit
    LIMIT 1;

    if (v_game_id is not null) then
        -- update time
        SELECT chess.game.next_move_player INTO v_next_move
        from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
        if v_next_move = 0::bit then
            begin
                SELECT chess.game.last_update INTO v_last_update from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
                SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), v_last_update) INTO v_date_diff;
                SELECT chess.game.player1_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
                SELECT v_left_time - make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_left_time;
                update chess.game set player1_time_left = v_left_time, last_update = NOW()
                WHERE chess.game.game_id = v_game_id;
            end;
        else
            begin
                SELECT chess.game.last_update INTO v_last_update from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
                SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), v_last_update) INTO v_date_diff;
                SELECT chess.game.player2_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
                SELECT v_left_time - make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_left_time;
                update chess.game set player2_time_left = v_left_time, last_update = NOW()
                WHERE chess.game.game_id = v_game_id;
            end;
        end if;
        begin
            call chess.add_game_message(p_game_id := v_game_id, p_add_user1 := 1::bit, p_add_user2 := 0::bit);
        end;
    else
        SELECT chess.game.game_id INTO v_game_id FROM chess.game WHERE
        chess.game.user_id2 = p_user_id and chess.game.is_playing = 1::bit
        LIMIT 1;
        if (v_game_id is not null) then
            SELECT chess.game.next_move_player INTO v_next_move
        from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
        if v_next_move = 0::bit then
            begin
                SELECT chess.game.last_update INTO v_last_update from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
                SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), v_last_update) INTO v_date_diff;
                SELECT chess.game.player1_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
                SELECT v_left_time - make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_left_time;
                update chess.game set player1_time_left = v_left_time, last_update = NOW()
                WHERE chess.game.game_id = v_game_id;
            end;
        else
            begin
                SELECT chess.game.last_update INTO v_last_update from chess.game WHERE chess.game.game_id=v_game_id LIMIT 1;
                SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), v_last_update) INTO v_date_diff;
                SELECT chess.game.player2_time_left INTO v_left_time FROM chess.game WHERE chess.game.game_id=v_game_id;
                SELECT v_left_time - make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_left_time;
                update chess.game set player2_time_left = v_left_time, last_update = NOW()
                WHERE chess.game.game_id = v_game_id;
            end;
        end if;
            begin
                call chess.add_game_message(p_game_id := v_game_id, p_add_user1 := 0::bit, p_add_user2 := 1::bit);
            end;
        end if;
    end if; 
end;

$BODY$