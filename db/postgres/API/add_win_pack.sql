CREATE OR REPLACE PROCEDURE chess.add_win_pack(
	p_game_id BIGINT)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_game chess.game%ROWTYPE;
    v_user_win INT;
    v_pack chess.packs%ROWTYPE;
    v_columns bigint;
    v_avail_packs integer[];
    v_data varchar;
BEGIN
    SELECT * into v_game FROM chess.game WHERE chess.game.game_id = p_game_id LIMIT 1;
    if v_game isnull then
        return;
    end if;
    if v_game.is_playing = 1::bit or v_game.game_result isnull then
        return;
    end if;
    if v_game.game_result = 0::bit then -- wins white
    begin
        select v_game.user_id1 into v_user_win;
    end;
    else
        select v_game.user_id2 into v_user_win; -- black wins
    end if;
    -- select win
    SELECT count(*) INTO v_columns FROM chess.packs;
    SELECT * into v_pack FROM chess.packs OFFSET floor(random() * v_columns) LIMIT 1;
    if v_pack isnull then
        return;
    end if;
    SELECT chess.players.user_packs INTO v_avail_packs from chess.players WHERE chess.players.user_id = v_user_win;
    if (v_pack.pack_id = ANY (v_avail_packs)) then -- already exists
        return;
    end if;
    UPDATE chess.players SET user_packs = array_append(v_avail_packs, v_pack.pack_id)
    WHERE chess.players.user_id = v_user_win;
    -- add message
    SELECT CONCAT('win_pack?new_pack=', v_pack.pack_name) INTO v_data;
    BEGIN
        call chess.add_message(p_data := v_data, p_user_id := v_user_win,
                               p_action_name := 'win_pack', p_add_delay := 1::bit);
    end;
END;

$BODY$;