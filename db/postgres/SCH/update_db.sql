CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO chess.packs (pack_name)
    SELECT 'pack11'
WHERE NOT EXISTS (
    SELECT 1 FROM chess.packs WHERE chess.packs.pack_name = 'pack11');

INSERT INTO chess.packs (pack_name)
    SELECT 'pack12'
WHERE NOT EXISTS (
    SELECT 1 FROM chess.packs WHERE chess.packs.pack_name = 'pack12');

INSERT INTO chess.packs (pack_name)
    SELECT 'pack13'
WHERE NOT EXISTS (
    SELECT 1 FROM chess.packs WHERE chess.packs.pack_name = 'pack13');

-- update user ratings
UPDATE chess.players SET rate = 1200 WHERE rate < 1200;
update chess.players SET user_packs = '{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}' WHERE login = 'super';