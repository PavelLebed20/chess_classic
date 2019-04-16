CREATE EXTENSION IF NOT EXISTS pgcrypto;

TRUNCATE chess.message_types cascade;
INSERT INTO chess.message_types (action_name, priority, description) VALUES
                                ('update_game', 1, 'Update current game state message'),
                                ('login', 2, 'User info about message');

TRUNCATE chess.players cascade;
INSERT INTO chess.players (login, password_salt, rate, email) VALUES
                          ('a', crypt('a', gen_salt('bf')), 1, 'amin1@mail.com'),
                          ('b', crypt('b', gen_salt('bf')), 1, 'amin2@mail.com');