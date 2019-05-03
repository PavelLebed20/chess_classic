CREATE OR REPLACE PROCEDURE chess.add_game_message_if_exists(
	p_user_id int)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_game_id bigint;
BEGIN
   LOCK TABLE ONLY chess.messages in share mode;

    SELECT chess.game.game_id INTO v_game_id FROM chess.game WHERE
          chess.game.user_id1 = p_user_id and chess.game.is_playing = 1::bit
    LIMIT 1;

    if (v_game_id is not null) then
        begin
            call chess.add_game_message(p_game_id := v_game_id, p_add_user1 := 1::bit, p_add_user2 := 0::bit);
        end;
    else
        SELECT chess.game.game_id INTO v_game_id FROM chess.game WHERE
        chess.game.user_id2 = p_user_id and chess.game.is_playing = 1::bit
        LIMIT 1;
        if (v_game_id is not null) then
            begin
                call chess.add_game_message(p_game_id := v_game_id, p_add_user1 := 0::bit, p_add_user2 := 1::bit);
            end;
        end if;
    end if; 
end;

$BODY$