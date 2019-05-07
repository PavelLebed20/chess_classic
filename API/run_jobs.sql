CREATE OR REPLACE PROCEDURE chess.run_jobs()
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    j_row chess.jobs%rowtype;
BEGIN
    --LOCK table only chess.jobs;
    for j_row in
        SELECT * FROM chess.jobs WHERE chess.jobs.next_execution_time <= NOW()
    LOOP
        begin
            EXECUTE CONCAT('call ', j_row.proc_name, '()');
        end;
    end loop;
    begin
        UPDATE chess.jobs SET next_execution_time = NOW() + delta_execution
        WHERE chess.jobs.next_execution_time <= NOW();
    end;
END;

$BODY$;