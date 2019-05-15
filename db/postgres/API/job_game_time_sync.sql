CREATE OR REPLACE PROCEDURE chess.job_game_time_sync()
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
  r_game chess.game%ROWTYPE;
  v_date_diff bigint;
  v_delta_time interval;
  v_left_time TIME;
  v_is_playing bit = 1::BIT;
  v_game_result bit = NULL;
  v_time_data varchar;
BEGIN
    for r_game in
        SELECT * FROM chess.game WHERE chess.game.is_playing = 1::bit
    LOOP
        begin
            SELECT 1::BIT INTO v_is_playing;
            SELECT NULL INTO v_game_result;
            if r_game.next_move_player = 0::bit then
                begin
                      SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), r_game.last_update) INTO v_date_diff;
                      SELECT make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_delta_time;
                      IF CAST(v_delta_time AS TIME) <= r_game.player1_time_left then
                          begin
                              SELECT r_game.player1_time_left - v_delta_time INTO v_left_time;
                          end;
                      else
                          SELECT TIME '00:00:00' into v_left_time;
                      end if;
                      if v_left_time = TIME '00:00:00' then
                         SELECT 0::bit into v_is_playing;
                         SELECT 1::bit into v_game_result; -- black win
                      end if;
                    begin
                        update chess.game set player1_time_left = v_left_time, last_update = NOW(),
                                 is_playing = v_is_playing, game_result = v_game_result
                          WHERE chess.game.game_id = r_game.game_id;
                    end;
                end;
            else
                begin
                      SELECT chess.date_time_diff_seconds(CAST(NOW() AS timestamp), r_game.last_update) INTO v_date_diff;
                      SELECT make_interval(secs := CAST(v_date_diff AS double precision)) INTO v_delta_time;
                      IF CAST(v_delta_time AS TIME) <= r_game.player2_time_left then
                          begin
                              SELECT r_game.player2_time_left - v_delta_time INTO v_left_time;
                          end;
                      else
                          SELECT TIME '00:00:00' into v_left_time;
                      end if;
                      if v_left_time = TIME '00:00:00' then
                         SELECT 0::bit into v_is_playing;
                         SELECT 1::bit into v_game_result; -- black win
                      end if;
                    begin
                        update chess.game set player2_time_left = v_left_time, last_update = NOW(),
                                 is_playing = v_is_playing, game_result = v_game_result
                          WHERE chess.game.game_id = r_game.game_id;
                    end;
                end;
            end if;
            -- update rate if need
            if v_is_playing = 0::bit then
              update chess.players set rate = case
                                                when v_game_result isnull then rate + r_game.draw_cost
                                                when v_game_result = 0::bit then rate + r_game.win_cost
                                                else rate - r_game.win_cost
                                              end
              WHERE user_id = r_game.user_id1;

              update chess.players set rate = case
                                                when v_game_result isnull then rate - r_game.draw_cost
                                                when v_game_result = 0::bit then rate - r_game.win_cost
                                                else rate + r_game.win_cost
                                              end
              WHERE user_id = r_game.user_id2;
          end if;
            -- add time update message
            begin
                SELECT CONCAT('update_time?',
                              'self_time=' , (SELECT chess.game.player1_time_left
                                               from chess.game WHERE chess.game.game_id=r_game.game_id
                                               LIMIT 1),
                              '&opponent_time=', (SELECT chess.game.player2_time_left
                                                  from chess.game WHERE chess.game.game_id=r_game.game_id
                                                  LIMIT 1),
                              '&opponent_rate=', (SELECT chess.players.rate FROM chess.players
                                                 WHERE chess.players.user_id=r_game.user_id2 limit 1),
                              '&is_playing=' ,  v_is_playing,
                              '&result=', v_game_result,
                              '&self_rate=', (SELECT chess.players.rate FROM chess.players
                                             WHERE chess.players.user_id=r_game.user_id1 limit 1)) into v_time_data;

                begin
                    call chess.add_message(p_data := v_time_data, p_user_id := r_game.user_id1,
                                           p_action_name := 'update_time');
                end;
                SELECT CONCAT('update_time?',
                              'self_time=' , (SELECT chess.game.player2_time_left
                                               from chess.game WHERE chess.game.game_id=r_game.game_id
                                               LIMIT 1),
                              '&opponent_time=', (SELECT chess.game.player1_time_left
                                                  from chess.game WHERE chess.game.game_id=r_game.game_id
                                                  LIMIT 1),
                              '&opponent_rate=', (SELECT chess.players.rate FROM chess.players
                                                 WHERE chess.players.user_id=r_game.user_id1 limit 1),
                              '&is_playing=' ,  v_is_playing,
                              '&result=', v_game_result,
                              '&self_rate=', (SELECT chess.players.rate FROM chess.players
                                             WHERE chess.players.user_id=r_game.user_id2 limit 1)) into v_time_data;

                begin
                    call chess.add_message(p_data := v_time_data, p_user_id := r_game.user_id2,
                                           p_action_name := 'update_time');
                end;
            end;
            if v_is_playing = 0::bit then
                call chess.add_win_pack(r_game.game_id);
            end if;
        end;
    end loop;
END;

$BODY$;