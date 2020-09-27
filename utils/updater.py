import importlib
import discord
from discord.ext import commands

importlib.import_module("database")

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.database = bot.get_cog("Database")

	@commands.command()
	async def add_channel(self, ctx, channel: discord.TextChannel):
		self.database.add_server(ctx.guild.id, channel.id)
		await ctx.send(f"Successfully set {channel} as a necromancy channel for this server.")

def setup(bot):
    bot.add_cog(Updater(bot))