do $$
begin
	call chess.game_start(
		p_user_id1 := 1,
		p_user_id2 := 2,
		p_game_time := TIME '00:03:00' , -- 3 minutes long game
		p_adding_time := 0,
		p_user1_side := null, -- (null - any, 0::bit - white, 1::bit - black)
		p_user2_side := null  -- (null - any, 0::bit - white, 1::bit - black)
);

	call chess.find_pair(
		p_user_id := 2,
		p_low_rate := 0,
		p_high_rate := 5000,
		p_adding_time := 0,
		p_game_time := TIME '00:03:00',
		p_side := null
);
end;
$$;