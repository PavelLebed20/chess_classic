CREATE OR REPLACE FUNCTION chess.get_messages(
  p_request_id bigint,
	p_max_count integer default 1000,
	p_delta_over_time TIME default TIME '00:01:00') RETURNS table(user_id int, data varchar) AS $$
DECLARE
    v_over_time TIMESTAMP;
BEGIN
  SELECT NOW() - p_delta_over_time into v_over_time;

begin
  LOCK TABLE ONLY chess.messages;
  UPDATE chess.messages set request_id = p_request_id, send_time = NOW() WHERE message_id in
                                                                            (SELECT distinct on (chess.messages.user_id)
                                                                             chess.messages.message_id from chess.messages
                                                                             WHERE request_id < 0 or
                                                                             (chess.messages.send_time NOTNULL
                                                                              and chess.messages.send_time <
                                                                              v_over_time) ORDER BY
                                            chess.messages.user_id, chess.messages.priority DESC LIMIT p_max_count);
commit;

  RETURN QUERY SELECT chess.messages.user_id,
                      CAST (CONCAT(chess.messages.data, '&request_id=', CAST(p_request_id AS VARCHAR)) AS VARCHAR)
  FROM chess.messages WHERE chess.messages.request_id = p_request_id;
END;

$$ LANGUAGE 'plpgsql';