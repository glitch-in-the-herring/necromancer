import sqlite3

conn = sqlite3.connect("test.db")
c = conn.cursor()

def add_server(guild_id, channel_id):
	c.execute("INSERT OR REPLACE INTO test (guild_id, channel_id) VALUES (?, ?)", [guild_id, channel_id])
	conn.commit()