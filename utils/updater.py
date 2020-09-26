import discord
from discord.ext import commands

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	database = self.bot.get_cog("Database")

	@commands.command
	async def test(self, ctx):
		database.add_server("this", "works")

def setup(bot):
    bot.add_cog(Database(bot))