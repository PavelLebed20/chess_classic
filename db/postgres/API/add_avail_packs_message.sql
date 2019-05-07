CREATE OR REPLACE PROCEDURE chess.add_avail_packs_message(
	p_user_id int )
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_avail_packs integer[];
    v_pack_id int;
    v_packs_str varchar;
    v_pack_name varchar(300);
begin
    select chess.players.user_packs into v_avail_packs
    from chess.players WHERE chess.players.user_id = p_user_id;
    if v_avail_packs isnull then
      return;
    end if;
    SELECT 'avail_packs?packs=' into v_packs_str;
    FOREACH v_pack_id IN ARRAY v_avail_packs
    LOOP
        SELECT chess.packs.pack_name INTO v_pack_name from chess.packs WHERE chess.packs.pack_id = v_pack_id;
        SELECT CONCAT(v_packs_str, v_pack_name, ',') INTO v_packs_str;
    END LOOP;
    select substr(v_packs_str, 1, length(v_packs_str) - 1) into v_packs_str;
    begin
        call chess.add_message(v_packs_str, p_user_id, 'avail_packs');
    end;
end;

$BODY$