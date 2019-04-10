CREATE EXTENSION IF NOT EXISTS pgcrypto;
LANGUAGE 'plpgsql';

TRUNCATE chess.message_types cascade;
INSERT INTO chess.message_types (action_name, priority, description) VALUES
                                ('update_game', 1, 'Update current game state message'),
                                ('login', 2, 'User info about message');

TRUNCATE chess.players cascade;
INSERT INTO chess.players (login, password_salt, rate, email) VALUES
                          ('admin1', crypt('admin1', gen_salt('bf')), 3000, 'amin1@mail.com'),
                          ('admin2', crypt('admin2', gen_salt('bf')), 3000, 'amin2@mail.com');