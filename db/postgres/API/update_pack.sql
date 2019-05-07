CREATE OR REPLACE PROCEDURE chess.update_pack(
	p_user_id int,
	p_pack_name varchar(300))
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_pack_id int;
    v_avail_packs integer[];
BEGIN
  select chess.players.user_packs into v_avail_packs
    from chess.players WHERE chess.players.user_id = p_user_id;
  select chess.packs.pack_id into v_pack_id from chess.packs WHERE chess.packs.pack_name = p_pack_name;
  if v_pack_id is null then
      return;
  end if;
  if v_avail_packs isnull or (SELECT v_pack_id != ALL(v_avail_packs)) then
      return;
  end if;
  UPDATE chess.players set current_pack = v_pack_id
  WHERE chess.players.user_id = p_user_id;
  UPDATE chess.game set player1_pack = v_pack_id
  where chess.game.user_id1 = p_user_id and chess.game.is_playing = 1::bit;
  UPDATE chess.game set player2_pack = v_pack_id
  where chess.game.user_id2 = p_user_id and chess.game.is_playing = 1::bit;
END;
$BODY$;