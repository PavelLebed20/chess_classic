CREATE OR REPLACE PROCEDURE chess.add_message(
	p_user_id integer)
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
BEGIN
  DELETE FROM chess.pairing WHERE chess.pairing.user_id = p_user_id;
END;

$BODY$;