CREATE TABLE scores (
	user_id INTEGER NOT NULL,
	guild_id INTEGER NOT NULL,
	score INTEGER,
	count INTEGER,
	PRIMARY KEY(user_id, guild_id)
);
CREATE TABLE guilds (
	guild_id INTEGER NOT NULL,
	channel_id INTEGER NOT NULL,
	last_author_id INTEGER,
	last_timestamp TEXT,
	mode INTEGER NOT NULL,
	counting INTEGER NOT NULL,
	PRIMARY KEY(guild_id)
);
