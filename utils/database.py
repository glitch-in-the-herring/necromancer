import sqlite3

conn = sqlite3.connect("necromancy.db")
c = conn.cursor()

def commit():
	conn.commit()


# Adds or updates channel_id and guild_id in the guilds table
def update_server(guild_id, channel_id):
	c.execute("INSERT OR REPLACE INTO guilds (guild_id, channel_id, last_author_id, last_timestamp) VALUES (?, ?, ?, ?)", [guild_id, channel_id, None, None])


# Updates the last message in a game channel
def update_last_message(guild_id, author_id, timestamp):
	c.execute("UPDATE guilds SET last_author_id = ?, last_timestamp = ? WHERE guild_id = ?", [author_id, timestamp, guild_id])


# Adds or updates the score in the scores table
def update_score(guild_id, user_id, score):
	c.execute("INSERT OR REPLACE INTO scores (guild_id, user_id, score) VALUES (?, ?, ?)", [guild_id, user_id, score])


# Clears an entire guild's score
def clear_score(guild_id):
	c.execute("DELETE FROM scores WHERE guild_id = ?", [guild_id])


# Retrieves the current guild's game channel's ID
def retrieve_channel(guild_id):
	try:
		return c.execute("SELECT channel_id FROM guilds WHERE guild_id = ?", [guild_id]).fetchone()[0]
	except TypeError:
		return None


# Retrieves the last message in a channel
def retrieve_last_message(guild_id):
	try:
		return c.execute("SELECT last_author_id, last_timestamp FROM guilds WHERE guild_id = ?", [guild_id]).fetchone()
	except TypeError:
		return None


# Retrieves the current user's score in the guild
def retrieve_score(guild_id, user_id):
	try:
		return c.execute("SELECT score FROM scores WHERE guild_id = ? AND user_id = ?", [guild_id, user_id]).fetchone()[0]
	except TypeError:
		return 0


# Retrieves the top 10 players in the guild
def retrieve_top_ten(guild_id):
	return c.execute("SELECT user_id, score FROM scores where guild_id = ? ORDER BY score DESC, user_id DESC LIMIT 10", [guild_id])


# Retrieves all players' scores in the guild
def retrieve_guild_scores(guild_id):
	return c.execute("SELECT score FROM scores where guild_id = ? ORDER BY score DESC, user_id DESC", [guild_id])