CREATE OR REPLACE PROCEDURE chess.add_pairings_list(
p_user_id int
)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_user_rate int;
    v_pairing_row chess.pairing%rowtype;
    v_pairing_list_data varchar;
    v_user chess.players%rowtype;
BEGIN
    SELECT chess.players.rate into v_user_rate
    FROM chess.players WHERE chess.players.user_id = p_user_id;
    IF p_user_id isnull then
        return;
    end if;
    SELECT 'pairing_list?pairing_list=' into v_pairing_list_data;

    FOR v_pairing_row IN
        SELECT * FROM chess.pairing
        WHERE v_user_rate between v_pairing_row.low_rate - 1 and v_pairing_row.high_rate
    LOOP

        SELECT * INTO v_user FROM chess.players WHERE chess.players.user_id = v_pairing_row.user_id limit 1;
        SELECT CONCAT(v_pairing_list_data,
                      v_pairing_row.pairing_id, ',',
                      v_user.login, ',',
                      v_user.rate, ',',
                      v_pairing_row.game_time, ',',
                      v_pairing_row.adding_time, ';') into v_pairing_list_data;
    END LOOP;

    begin
        call chess.add_message(p_data := v_pairing_list_data, p_user_id := p_user_id,
                               p_action_name := 'pairing_list');
    end;
end;

$BODY$