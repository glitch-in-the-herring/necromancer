import sqlite3
from discord.ext import commands

conn = sqlite3.connect("../test.db")
c = conn.cursor()

class Databse(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def add_server(guild_id, channel_id):
		c.execute("INSERT OR REPLACE INTO test (guild_id, channel_id) VALUES (?, ?)", [guild_id, channel_id])

def setup(bot):
    bot.add_cog(Database(bot))