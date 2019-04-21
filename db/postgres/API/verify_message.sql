CREATE OR REPLACE PROCEDURE chess.verify_message(
	p_request_id bigint,
	p_user_id integer)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
BEGIN
  UPDATE chess.messages SET send_time = NULL WHERE request_id = p_request_id AND user_id = p_user_id;
END;
$BODY$;
