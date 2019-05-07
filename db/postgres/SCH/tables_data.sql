CREATE EXTENSION IF NOT EXISTS pgcrypto;

TRUNCATE chess.message_types cascade;
INSERT INTO chess.message_types (action_name, priority, description, resend_time, resend_stop_time) VALUES
                                ('update_time', 1, 'Update current game time message', TIME '00:00:05', TIME '00:01:00'),
                                ('update_game', 2, 'Update current game state message', TIME '00:00:07', TIME '00:01:00'),
                                ('login', 3, 'User info about message', TIME '00:00:05', TIME '00:01:00');

TRUNCATE chess.players cascade;
INSERT INTO chess.players (login, password_salt, rate, email, verified) VALUES
                          ('a', crypt('a', gen_salt('bf')), 1, 'amin1@mail.com', 1::bit),
                          ('b', crypt('b', gen_salt('bf')), 1, 'amin2@mail.com', 1::bit);

-- add jobs
TRUNCATE chess.jobs cascade;
INSERT INTO chess.jobs (proc_name, delta_execution) VALUES
                       ('chess.job_stop_messages', TIME '00:01:00'),
                       ('chess.job_game_time_sync', TIME '00:00:05');