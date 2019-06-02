CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- update user ratings
UPDATE chess.players SET rate = 1200 WHERE rate < 1200;
update chess.players SET user_packs = '{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}' WHERE login = 'super';