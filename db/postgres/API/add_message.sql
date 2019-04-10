CREATE OR REPLACE PROCEDURE chess.add_message(
	p_data varchar,
	p_user_id integer,
	p_action_name varchar)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
    v_message_type_id int;
    v_total_rows int;
BEGIN
  SELECT chess.message_types.message_type_id INTO v_message_type_id from chess.message_types where
                                                                         chess.message_types.action_name = p_action_name;

  BEGIN
  --LOCK TABLE ONLY chess.game;
    -- update message data if have such message in database not send
    update chess.messages set data = p_data, request_id = -1, send_time = null where user_id = p_user_id and
                                                                   message_type_id = v_message_type_id;
    GET DIAGNOSTICS v_total_rows := ROW_COUNT;
    if v_total_rows > 0 then
        return;
    end if;
    -- otherwise add new
    INSERT INTO chess.messages(data, user_id, message_type_id, priority) VALUES (p_data, p_user_id,
                                                                                 v_message_type_id,
                                                                                 (SELECT chess.message_types.priority
                                                                                  from chess.message_types where
                                                                                  chess.message_types.action_name =
                                                                                  p_action_name));
  END;
END;

$BODY$;