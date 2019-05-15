CREATE OR REPLACE PROCEDURE chess.add_message(
	p_data varchar,
	p_user_id integer,
	p_action_name varchar,
	p_add_delay bit default 0::bit)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_message_type_id int;
    v_total_rows int;
    v_request_id int;
    v_send_time TIMESTAMP;
BEGIN
  SELECT chess.message_types.message_type_id INTO v_message_type_id from chess.message_types where
                                                                         chess.message_types.action_name = p_action_name;
  if p_add_delay = 1::bit then
      select 0 into v_request_id;
      select NOW() INTO v_send_time;
  else
      select -1 into v_request_id;
      select NULL INTO v_send_time;
  end if;

  BEGIN
    --LOCK TABLE ONLY chess.game;
    -- update message data if have such message in database not send
    update chess.messages set data = p_data, request_id = v_request_id, send_time = v_send_time, add_time = NOW()
    where user_id = p_user_id and message_type_id = v_message_type_id;
    GET DIAGNOSTICS v_total_rows := ROW_COUNT;
    if v_total_rows > 0 then
        return;
    end if;
    -- otherwise add new
    INSERT INTO chess.messages(request_id, send_time, data, user_id, message_type_id, priority,
                               resend_time, resend_stop_time) VALUES (v_request_id,
                                                                      v_send_time,
                                                                      p_data,
                                                                     p_user_id,
                                                                     v_message_type_id,
                                                                     (SELECT chess.message_types.priority
                                                                      from chess.message_types where
                                                                      chess.message_types.action_name =
                                                                      p_action_name),
                                                                      (SELECT chess.message_types.resend_time
                                                                      from chess.message_types where
                                                                      chess.message_types.action_name =
                                                                      p_action_name),
                                                                      (SELECT chess.message_types.resend_stop_time
                                                                      from chess.message_types where
                                                                      chess.message_types.action_name =
                                                                      p_action_name));
  END;
END;

$BODY$;