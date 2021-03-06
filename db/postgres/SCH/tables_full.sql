--LANGUAGE 'plpgsql';

DROP SCHEMA IF EXISTS chess cascade;
CREATE SCHEMA chess;

-- pack table create
DROP TABLE IF EXISTS chess.packs;
CREATE TABLE chess.packs
(
    pack_name varchar(300),
    pack_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

-- INDEXES OBTAIN
create index packs_pack_name_idx ON chess.packs(pack_name);
create index packs_pack_id_idx ON chess.packs(pack_id);

-- end of pack table creation

-- Players table create
DROP TABLE IF EXISTS chess.players CASCADE;
CREATE TABLE  chess.players
(
	user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	login varchar(128) NOT NULL UNIQUE,
	password_salt varchar(73) NOT NULL, -- use as bf salt
	rate INT NOT NULL DEFAULT 0 CONSTRAINT rate_value CHECK (rate >= 0 and rate <= 5000),
	email varchar(128) NOT NULL UNIQUE,
	verified bit NOT NULL DEFAULT 0::bit,
	registration_time timestamp NOT NULL DEFAULT NOW(),
	last_update timestamp NOT NULL DEFAULT NOW(),
    user_packs integer[] NOT NULL DEFAULT '{1}',
    current_pack int NOT NULL DEFAULT 1 references chess.packs(pack_id)
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
	auth_code varchar(64) NOT NULL,
	send bit DEFAULT 0::bit
);

-- End of AuthCodes table create

-- Game table create
DROP TABLE IF EXISTS chess.game;
CREATE TABLE chess.game
(
    game_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	user_id1 INT NOT NULL references chess.players(user_id), -- plays white
	user_id2 INT NOT NULL references chess.players(user_id), -- plays black
	board varchar(64) DEFAULT NULL,
	win_cost INT NOT NULL DEFAULT 0 CONSTRAINT win_cost_value CHECK (win_cost >= 0 and win_cost <= 45),
	draw_cost INT NOT NULL DEFAULT 0 CONSTRAINT draw_cost_value CHECK (draw_cost >= 0 and draw_cost <= 45),
	next_move_player bit NOT NULL DEFAULT 0::bit, -- (0 - white move, 1 - black move)
	adding_time INT NOT NULL DEFAULT 0 CONSTRAINT adding_time_value CHECK (adding_time >= 0 and adding_time <= 3600), -- in seconds
	player1_time_left TIME,  -- null for not timed game
	player2_time_left TIME,  -- null for not timed game
	registration_time timestamp NOT NULL DEFAULT NOW(),
	last_update timestamp NOT NULL DEFAULT NOW(),
	is_playing bit NOT NULL DEFAULT 1::bit,
	game_result bit DEFAULT NULL, -- (0 - white, 1 - black, NULL - draw)
	-- packs info
	player1_pack int not null,
	player2_pack int not null
);

-- INDEXES OBTAIN
create index game_game_id ON chess.game(game_id);
create index game_user_id1 ON chess.game(user_id1);
create index game_user_id2 ON chess.game(user_id2);
create index game_is_playing ON chess.game(is_playing);
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
create index pairing_pairing_id ON chess.pairing(pairing_id);
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
	resend_time TIME NOT NULL,
	resend_stop_time TIME NOT NULL,
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
    resend_time TIME NOT NULL,
    resend_stop_time TIME NOT NULL,
    add_time timestamp DEFAULT NOW()
);

DROP sequence if exists requests_seq;
create sequence requests_seq maxvalue 9223372036854775807;

-- INDEXES OBTAIN
create index messages_id_idx ON chess.messages(message_id);
create index messages_send_time_idx ON chess.messages(send_time);
create index messages_user_id_idx ON chess.messages(user_id);
create index messages_priority_idx ON chess.messages(priority);
create index messages_add_time ON chess.messages(add_time);
-- End of Message table create

-- Job table create
DROP TABLE IF EXISTS chess.jobs;
CREATE TABLE chess.jobs
(
    proc_name varchar(1000),
    delta_execution TIME,
    next_execution_time timestamp DEFAULT NOW()
);
-- INDEXES OBTAIN
create index jobs_next_execution_time_idx ON chess.jobs(next_execution_time);
-- END OF Job table create