CREATE OR REPLACE function chess.get_request()
	RETURNS bigint AS $$
DECLARE
  v_request_id bigint;
  v_tmp bigint;
BEGIN
  SELECT nextval('requests_seq')::bigint into v_request_id;
  -- reset sequence
  if v_request_id = 9223372036854775807 then
      SELECT setval('requests_seq', 1, false) into v_tmp;
  end if;

  RETURN v_request_id;
END;

$$ LANGUAGE plpgsql;