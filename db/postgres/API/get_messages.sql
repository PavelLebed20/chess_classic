CREATE OR REPLACE FUNCTION chess.get_messages(
    p_request_id bigint,
	p_max_count integer default 1000) RETURNS table(user_id int, data varchar) AS $$
DECLARE
    v_cnt int;
    v_tmp bigint;
BEGIN
    LOCK TABLE ONLY chess.messages in share row exclusive mode;
begin
  UPDATE chess.messages set request_id = 0, send_time = NULL WHERE
                                                         request_id <> 0 and
                                                         chess.messages.send_time NOTNULL
                                                          and chess.messages.add_time <
                                                          NOW() - chess.messages.resend_stop_time;
end;

begin
  UPDATE chess.messages set request_id = p_request_id, send_time = NOW() WHERE message_id in
                                                                            (SELECT distinct on (chess.messages.user_id)
                                                                             chess.messages.message_id from chess.messages
                                                                             JOIN chess.players on
                                                                          chess.players.user_id = chess.messages.user_id
                                                                          AND chess.players.online = 1::bit
                                                                             WHERE
                                                                                   request_id < 0 or
                                                                             (chess.messages.send_time NOTNULL
                                                                              and chess.messages.send_time <
                                                                              NOW() - chess.messages.resend_time) ORDER BY
                                            chess.messages.user_id, chess.messages.priority DESC LIMIT p_max_count);

  get diagnostics v_cnt = row_count;
  -- reset sequence value, it is not used
  if v_cnt = 0 then
      begin
          SELECT setval('requests_seq', p_request_id, false) into v_tmp;
      end;
  end if;
end;

  RETURN QUERY SELECT chess.messages.user_id,
                      CAST (CONCAT(chess.messages.data, '&request_id=', CAST(p_request_id AS VARCHAR)) AS VARCHAR)
  FROM chess.messages WHERE chess.messages.request_id = p_request_id;
END;

$$ LANGUAGE 'plpgsql';