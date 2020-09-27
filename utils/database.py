import sqlite3
from discord.ext import commands

conn = sqlite3.connect("necromancy.db")
c = conn.cursor()

class Database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def add_server(self, guild_id, channel_id):
		c.execute("INSERT OR REPLACE INTO guilds (guild_id, channel_id) VALUES (?, ?)", [guild_id, channel_id])
		conn.commit()

	def update_score(self, guild_id, user_id, score, penalty):
		c.execute("INSERT OR REPLACE INTO scores (guild_id, user_id, score, penalty) VALUES (?, ?, ?, ?)", [guild_id, user_id, score, penalty])

	def retrieve_channel(self, guild_id):
		return c.execute("SELECT channel_id FROM guilds WHERE guild_id = ?", [guild_id]).fetchone()[0]

def setup(bot):
    bot.add_cog(Database(bot))