--LANGUAGE 'plpgsql';

DROP SCHEMA IF EXISTS chess cascade;
CREATE SCHEMA chess;

-- Players table create
DROP TABLE IF EXISTS chess.players CASCADE;
CREATE TABLE  chess.players
(
	user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	login varchar(50) NOT NULL UNIQUE,
	password_salt varchar(73) NOT NULL, -- use as bf salt
	rate INT NOT NULL DEFAULT 0 CONSTRAINT rate_value CHECK (rate >= 0 and rate <= 5000),
	email varchar(50) NOT NULL UNIQUE,
	verified bit NOT NULL DEFAULT 0::bit,
	online bit NOT NULL DEFAULT 0::bit,
	registration_time timestamp NOT NULL DEFAULT NOW(),
	last_update timestamp NOT NULL DEFAULT NOW()
);
-- INDEXES OBTAIN
create index players_login_idx ON chess.players(login);
create index players_email_idx ON chess.players(email);

-- End of Players table create

-- AuthCodes table create
DROP TABLE IF EXISTS chess.auth_codes;
CREATE TABLE  chess.auth_codes
(
	user_id INT NOT NULL references chess.players(user_id) PRIMARY KEY,
	code_salt varchar(73) NOT NULL,
	verified bit NOT NULL DEFAULT 0::bit,
	generated_time timestamp NOT NULL DEFAULT NOW()
);

-- INDEXES OBTAIN
create index auth_codes_generated_time_idx ON chess.auth_codes(generated_time);

-- End of AuthCodes table create

-- Game table create
DROP TABLE IF EXISTS chess.game;
CREATE TABLE chess.game
(
    game_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_id1 INT NOT NULL references chess.players(user_id), -- plays white
	user_id2 INT NOT NULL references chess.players(user_id), -- plays black
	board bytea DEFAULT NULL,
	win_cost INT NOT NULL DEFAULT 0 CONSTRAINT win_cost_value CHECK (win_cost >= 0 and win_cost <= 45),
	draw_cost INT NOT NULL DEFAULT 0 CONSTRAINT draw_cost_value CHECK (draw_cost >= 0 and draw_cost <= 45),
	next_move_player bit NOT NULL DEFAULT 0::bit, -- (0 - white move, 1 - black move)
	adding_time INT NOT NULL DEFAULT 0 CONSTRAINT adding_time_value CHECK (adding_time >= 0 and adding_time <= 3600), -- in seconds
	player1_time_left TIME,  -- null for not timed game
	player2_time_left TIME,  -- null for not timed game
	registration_time timestamp NOT NULL DEFAULT NOW(),
	last_update timestamp NOT NULL DEFAULT NOW(),
	is_playing bit NOT NULL DEFAULT 1::bit,
	game_result bit DEFAULT NULL -- (0 - white, 1 - black, NULL - draw)
);
-- End of Game table create

-- Pairing table create
DROP TABLE IF EXISTS chess.pairing;
CREATE TABLE chess.pairing
(
    pairing_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_id INT NOT NULL references chess.players(user_id) UNIQUE,
	low_rate INT NOT NULL DEFAULT 0 CONSTRAINT low_rate_value CHECK (low_rate >= 0 and low_rate <= 5000),
	high_rate INT NOT NULL DEFAULT 5000
	     CONSTRAINT high_rate_value CHECK (high_rate >= 0 and high_rate <= 5000 and high_rate >= low_rate),
	side bit DEFAULT NULL, -- (0 - white, 1 - black, NULL - any),
	adding_time INT NOT NULL DEFAULT 0 CONSTRAINT adding_time_value CHECK (adding_time >= 0 and adding_time <= 3600), -- in seconds
	game_time TIME,  -- null for not timed game
	registration_time timestamp NOT NULL DEFAULT NOW()
);

-- INDEXES OBTAIN
create index pairing_registration_time_idx ON chess.pairing(registration_time);
create index pairing_user_id_idx ON chess.pairing(user_id);
create index pairing_adding_time_game_time_idx ON chess.pairing(adding_time, game_time);

-- End of Pairing table create

-- MessageTypes table create
DROP TABLE IF EXISTS chess.message_types CASCADE;
CREATE TABLE chess.message_types
(
    action_name varchar(64) NOT NULL,
    message_type_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	priority INT NOT NULL,
	description varchar(300) NOT NULL
);

-- INDEXES OBTAIN
create index message_types_action_name_idx ON chess.message_types(action_name);

-- End of MessageTypes table create

-- Message table create
DROP TABLE IF EXISTS chess.messages;
CREATE TABLE chess.messages
(
    message_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    request_id BIGINT NOT NULL DEFAULT -1,
    data varchar NOT NULL,
    user_id INT NOT NULL references chess.players(user_id),
    message_type_id INT NOT NULL references chess.message_types(message_type_id),
    priority INT NOT NULL,
    send_time timestamp DEFAULT NULL,
	byte_data bytea DEFAULT NULL
);

DROP sequence if exists requests_seq;
create sequence requests_seq maxvalue 9223372036854775807;

-- INDEXES OBTAIN
create index messages_send_time_idx ON chess.messages(send_time);
create index messages_user_id_idx ON chess.messages(user_id);
-- End of Message table create

