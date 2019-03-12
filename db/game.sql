USE [Chess]
GO
/****** Object:  Table [dbo].[auth_codes]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
/****** Object:  Table [dbo].[games]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[games](
	[game_id] [int] IDENTITY(1,1) NOT NULL,
	[user_id1] [int] NOT NULL,
	[user_id2] [int] NOT NULL,
	[board] [nvarchar](64) NOT NULL,
	[cost] [int] NOT NULL,
	[color] [bit] NOT NULL,
	[cur_player_num] [bit] NOT NULL,
 CONSTRAINT [games_game_id_primary] PRIMARY KEY CLUSTERED 
(
	[game_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [chess_games_player_id1_unique] UNIQUE NONCLUSTERED 
(
	[user_id1] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [chess_games_player_id2_unique] UNIQUE NONCLUSTERED 
(
	[user_id2] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[pairing]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[pairing](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [int] NOT NULL,
	[low_rate] [smallint] NULL,
	[high_rate] [smallint] NULL,
	[game_time] [smallint] NULL,
	[game_additional_time] [smallint] NULL,
 CONSTRAINT [chess_pairing_user_id_unique] UNIQUE NONCLUSTERED 
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[requests]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
GO
ALTER TABLE [dbo].[games] ADD  CONSTRAINT [DF_games_cost]  DEFAULT ((0)) FOR [cost]
GO
ALTER TABLE [dbo].[games] ADD  CONSTRAINT [DF_games_color]  DEFAULT ((0)) FOR [color]
GO
ALTER TABLE [dbo].[pairing] ADD  CONSTRAINT [DF_pairing_low_rate]  DEFAULT ((0)) FOR [low_rate]
GO
ALTER TABLE [dbo].[pairing] ADD  CONSTRAINT [DF_pairing_high_rate]  DEFAULT ((1000)) FOR [high_rate]
GO
ALTER TABLE [dbo].[pairing] ADD  CONSTRAINT [DF_pairing_game_time]  DEFAULT ((10)) FOR [game_time]
GO
ALTER TABLE [dbo].[pairing] ADD  CONSTRAINT [DF_pairing_game_additional_time]  DEFAULT ((0)) FOR [game_additional_time]
GO
ALTER TABLE [dbo].[requests] ADD  CONSTRAINT [DF_requests_request_status]  DEFAULT ((0)) FOR [request_status]
GO
ALTER TABLE [dbo].[auth_codes]  WITH CHECK ADD  CONSTRAINT [auth_codes_user_id_ref] FOREIGN KEY([user_id])
REFERENCES [dbo].[chess_users] ([user_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[auth_codes] CHECK CONSTRAINT [auth_codes_user_id_ref]
GO
ALTER TABLE [dbo].[games]  WITH CHECK ADD  CONSTRAINT [games_user_id1_ref] FOREIGN KEY([user_id1])
REFERENCES [dbo].[chess_users] ([user_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[games] CHECK CONSTRAINT [games_user_id1_ref]
GO
ALTER TABLE [dbo].[games]  WITH CHECK ADD  CONSTRAINT [games_user_id2_ref] FOREIGN KEY([user_id2])
REFERENCES [dbo].[chess_users] ([user_id])
GO
ALTER TABLE [dbo].[games] CHECK CONSTRAINT [games_user_id2_ref]
GO
ALTER TABLE [dbo].[pairing]  WITH CHECK ADD  CONSTRAINT [pairing_user_id_ref] FOREIGN KEY([user_id])
REFERENCES [dbo].[chess_users] ([user_id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[pairing] CHECK CONSTRAINT [pairing_user_id_ref]
GO
/****** Object:  StoredProcedure [dbo].[chess_games_start_game]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_games_start_game]
@user_id1 int,
@user_id2 int
AS
/*
Вызывается из процедуры chess_pairing_start_find_game() при нахождении подходящей пары.
Условия: игроки уникальны(игрок не может одновременно участвовать более чем в 1 игре)
Доска инициализируются по дефолту. Стоимость по дефолту = 0. Цвет - рандомное bit значение(будем считать если 0 то первый - белый).
Добавляем запись в таблицу games.
Вызываем chess_stop_find_game(user_id1),chess_stop_find_game(user_id2).
Отправляем сообщение клиентам о начале игры(чтобы клиенты перешли на экран игры).
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_games_stop_game]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_games_stop_game]
@game_id int,
@player_win bit
AS
/*
Вызывается сервером при мате/пате/сдаче. Или из job, которая проверяет отключение клиента от сервера.
Происходит пересчет и обновление рейтингов (если player_win = 0 победил первый игрок). 
После выполнения процедуры сервер посылает клиентам посылается сообщение об окончании игры - там оно обрабатывается как переход к главному экрану.
Запись об игре удаляется.
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_games_update_field]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_games_update_field]
@game_id int,
@cur_player_num bit,
@board nvarchar(64)
AS
/*
Вызывается сервером при изменении положения фигур на поле.
Проверяется, что данный игрок(cur_player_num) сейчас может ходить.
Здесь выполняем UPDATE games[game_id].board.
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_pairing_start_find_game]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_pairing_start_find_game]
@user_id int
AS
/*
Условия: игрок должен быть уникален(нельзя искать сразу несколько игр)
1)Найти соперника
Если не найден соперник вернуть none
Если соперник найден - начать игру(start_game(user1,user2)). 
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_pairing_stop_find_game]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_pairing_stop_find_game]
@user_id int
AS
/*
Вызывается клиентом при отмене поиска игры или сервером при начале игры
*/
GO
