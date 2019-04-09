CREATE OR REPLACE FUNCTION chess.get_messages(
  p_request_id bigint,
	p_max_count integer default 1000,
	p_delta_over_time TIME default TIME '00:01:00') RETURNS table(user_id int, data varchar) AS $$
DECLARE
    v_over_time TIMESTAMP;
BEGIN
  SELECT NOW() - p_delta_over_time into v_over_time;

  LOCK TABLE ONLY chess.messages;

  DROP TABLE IF EXISTS message_ids_tmp;
  CREATE TEMP TABLE message_ids_tmp
  (
    message_id bigint
  );


  INSERT INTO message_ids_tmp (SELECT distinct on (chess.messages.user_id) chess.messages.message_id from chess.messages
                                                                             WHERE request_id < 0 or
                                                                             (chess.messages.send_time NOTNULL
                                                                              and chess.messages.send_time <
                                                                              v_over_time) LIMIT p_max_count);

  UPDATE chess.messages set request_id = p_request_id, send_time = NOW() WHERE message_id in
                                                                               (SELECT message_id FROM message_ids_tmp);

  DROP TABLE IF EXISTS message_ids_tmp;

  RETURN QUERY SELECT chess.messages.user_id, chess.messages.data FROM chess.messages WHERE chess.messages.request_id = p_request_id;
END;

$$ LANGUAGE 'plpgsql';