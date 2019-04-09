CREATE OR REPLACE function chess.get_request()
	RETURNS bigint AS $$
DECLARE
  v_request_id bigint;
BEGIN
  SELECT nextval('requests_seq')::bigint into v_request_id;
  RETURN v_request_id;
END;

$$ LANGUAGE plpgsql;