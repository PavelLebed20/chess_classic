CREATE OR REPLACE FUNCTION chess.get_messages(
  p_request_id bigint,
	p_max_count integer default 1000,
	p_delta_over_time TIME default TIME '00:00:02') RETURNS table(user_id int, data varchar, byte_data bytea) AS $$
DECLARE
    v_over_time TIMESTAMP;
BEGIN
  SELECT NOW() - p_delta_over_time into v_over_time;

begin
  LOCK TABLE ONLY chess.messages in share row exclusive mode;
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
                                                                              v_over_time) ORDER BY
                                            chess.messages.user_id, chess.messages.priority DESC LIMIT p_max_count);
end;

  RETURN QUERY SELECT chess.messages.user_id,
                      CAST (CONCAT(chess.messages.data, '&request_id=', CAST(p_request_id AS VARCHAR)) AS VARCHAR),
                      chess.messages.byte_data
  FROM chess.messages WHERE chess.messages.request_id = p_request_id;
END;

$$ LANGUAGE 'plpgsql';