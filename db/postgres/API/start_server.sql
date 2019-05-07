CREATE OR REPLACE PROCEDURE chess.start_server()
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
BEGIN
  UPDATE chess.messages SET request_id = 0, send_time = NULL;
END;
$BODY$;
