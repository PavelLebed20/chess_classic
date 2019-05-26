CREATE OR REPLACE PROCEDURE chess.surrender(
	p_user_id INT)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_game chess.game%ROWTYPE;
BEGIN
    LOCK TABLE only chess.game;
    SELECT * INTO v_game FROM chess.game WHERE
    (chess.game.user_id1 = p_user_id or chess.game.user_id2 = p_user_id) and chess.game.is_playing = 1::bit limit 1;

    IF v_game isnull then
        return;
    end if;

    UPDATE chess.game SET is_playing = 0::bit, game_result = case when v_game.user_id1 = p_user_id then 1::bit -- win black
                                                             else 0::bit end WHERE chess.game.game_id = v_game.game_id; -- win white

    begin
        call chess.add_game_message(p_game_id := v_game.game_id, p_add_user1 := 1::bit, p_add_user2 := 1::bit);
    end;

    begin
        call chess.add_win_pack(v_game.game_id);
    end;

END;

$BODY$;