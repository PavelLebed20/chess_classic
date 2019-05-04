CREATE EXTENSION IF NOT EXISTS pgcrypto;

TRUNCATE chess.message_types cascade;
INSERT INTO chess.message_types (action_name, priority, description, resend_time, resend_stop_time) VALUES
                                ('update_game', 1, 'Update current game state message', TIME '00:00:10', TIME '00:01:00'),
                                ('login', 2, 'User info about message', TIME '00:00:05', TIME '00:01:00');

TRUNCATE chess.players cascade;
INSERT INTO chess.players (login, password_salt, rate, email, verified) VALUES
                          ('a', crypt('a', gen_salt('bf')), 1, 'amin1@mail.com', 1::bit),
                          ('b', crypt('b', gen_salt('bf')), 1, 'amin2@mail.com', 1::bit);