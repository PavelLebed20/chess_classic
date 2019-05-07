CREATE EXTENSION IF NOT EXISTS pgcrypto;

TRUNCATE chess.message_types cascade;
INSERT INTO chess.message_types (action_name, priority, description, resend_time, resend_stop_time) VALUES
                                ('avail_packs', 1, 'User available packs', TIME '00:00:20', TIME '00:01:00'),
                                ('update_time', 2, 'Update current game time message', TIME '00:00:05', TIME '00:01:00'),
                                ('update_game', 3, 'Update current game state message', TIME '00:00:07', TIME '00:01:00'),
                                ('login', 4, 'User info about message', TIME '00:00:05', TIME '00:01:00');

TRUNCATE chess.packs cascade;
INSERT INTO chess.packs (pack_name) values
                                          ('pack0'),
                                          ('pack1'),
                                          ('pack2'),
                                          ('pack3'),
                                          ('pack4'),
                                          ('pack5'),
                                          ('pack6'),
                                          ('pack7'),
                                          ('pack8'),
                                          ('pack9'),
                                          ('pack10'),
                                          ('pack11');

TRUNCATE chess.players cascade;
INSERT INTO chess.players (login, password_salt, rate, email, verified, user_packs) VALUES
                          ('a', crypt('a', gen_salt('bf')), 1, 'amin1@mail.com', 1::bit, '{1, 2, 3, 4, 5, 6}'),
                          ('b', crypt('b', gen_salt('bf')), 1, 'amin2@mail.com', 1::bit, '{1, 2, 3, 4, 5, 6}');

-- add jobs
TRUNCATE chess.jobs cascade;
INSERT INTO chess.jobs (proc_name, delta_execution) VALUES
                       ('chess.job_stop_messages', TIME '00:01:00'),
                       ('chess.job_game_time_sync', TIME '00:00:05');