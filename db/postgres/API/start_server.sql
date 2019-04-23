CREATE OR REPLACE PROCEDURE chess.start_server()
LANGUAGE 'plpgsql'

AS $BODY$
DECLARE
BEGIN
  UPDATE chess.players SET online = 0::bit;
END;
$BODY$;
