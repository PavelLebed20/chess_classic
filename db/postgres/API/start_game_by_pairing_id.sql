CREATE OR REPLACE PROCEDURE chess.start_game_by_pairing_id(
p_user_id int,
p_pairing_id bigint
)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_pairing chess.pairing%rowtype;
    v_user chess.players%rowtype;
BEGIN
   LOCK TABLE ONLY chess.pairing;
   SELECT * INTO v_user FROM chess.players WHERE chess.players.user_id = p_user_id;
   if v_user isnull then
       return;
   end if;
   SELECT * INTO v_pairing FROM chess.pairing WHERE chess.pairing.pairing_id = p_pairing_id and
                                                    chess.pairing.user_id != p_user_id and
                                                    v_user.rate between chess.pairing.low_rate - 1 and
                                                    chess.pairing.high_rate;
   if v_pairing isnull then
       begin
           call chess.add_pairings_list(p_user_id := p_user_id);
           return;
       end;
   end if;

   DELETE FROM chess.pairing WHERE chess.pairing.pairing_id = p_pairing_id;

   begin
	call chess.game_start(
		p_user_id1 := p_user_id,
		p_user_id2 := v_pairing.user_id,
		p_game_time := v_pairing.game_time,
		p_adding_time := v_pairing.adding_time,
		p_user1_side := null,
		p_user2_side := v_pairing.side);
   end;
end;

$BODY$