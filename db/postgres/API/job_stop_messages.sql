CREATE OR REPLACE PROCEDURE chess.job_stop_messages()
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
BEGIN
  --LOCK TABLE ONLY chess.messages in share row exclusive mode;
  begin
  -- disable old messages
    UPDATE chess.messages set request_id = 0, send_time = NULL WHERE
                                                         (request_id <> 0 and
                                                         chess.messages.send_time NOTNULL
                                                          and chess.messages.add_time <
                                                          NOW() - chess.messages.resend_stop_time);
    end;
END;
$BODY$;