USE [Chess]
GO
/****** Object:  Table [dbo].[auth_codes]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_codes](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [int] NOT NULL,
	[code] [nvarchar](50) NOT NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[chess_users]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[chess_users](
	[login] [nvarchar](50) NOT NULL,
	[password] [nvarchar](50) NOT NULL,
	[rate] [int] NOT NULL CONSTRAINT [DF_chess_users_rating]  DEFAULT ((0)),
	[email] [nvarchar](50) NOT NULL,
	[auth_status] [bit] NOT NULL CONSTRAINT [DF_chess_users_auth_status]  DEFAULT ((0)),
	[user_id] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [chess_users_user_id_primary] PRIMARY KEY CLUSTERED 
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [chess_email_unique] UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [chess_login_unique] UNIQUE NONCLUSTERED 
(
	[login] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

/****** Object:  StoredProcedure [dbo].[chess_users_auth]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_users_auth]
@login nvarchar(50),
@password nvarchar(50),
@email nvarchar(50)
AS
/*
1)Проверить, что login and mail уникальны. Добавить в базу запись с переданными данными. 
2)Сгенерировать код(auth_code) и добавить в таблицу auth_codes запись с (user_id, auth_code).  
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_users_auth_confirm]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_users_auth_confirm]
@login nvarchar(50),
@code nvarchar(50)
AS

/*
1)Проверяется совпадение кода в таблице auth_codes с переданным кодом. При совпадении ставим auth_status = true. 
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_users_login]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_users_login]
@login nvarchar(50),
@password nvarchar(50)
AS

/*
1)Проверяем соответствуют ли переданные логин и пароль значениям в таблице (выбираем только из авторизированных пользователей). 
2)Устанавливаем login_status = true. ( это не точно )
3)Возвращаем клиенту инфо об игроке (id, login, rate). В случае ошибки вернём error с текстом ошибки.
*/
GO
/****** Object:  StoredProcedure [dbo].[chess_users_logout]    Script Date: 12.03.2019 22:31:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[chess_users_logout]
@user_id int
AS

GO
