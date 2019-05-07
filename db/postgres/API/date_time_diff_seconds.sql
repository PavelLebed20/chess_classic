CREATE OR REPLACE function chess.date_time_diff_seconds(
	p_bigger_time timestamp,
	p_lower_time timestamp)
	RETURNS bigint AS $$
DECLARE
BEGIN
return ((DATE_PART('day', p_bigger_time - p_lower_time) * 24 +
         DATE_PART('hour', p_bigger_time - p_lower_time)) * 60 +
         DATE_PART('minute', p_bigger_time - p_lower_time)) * 60 +
         DATE_PART('second', p_bigger_time - p_lower_time);
end;

$$ LANGUAGE plpgsql;