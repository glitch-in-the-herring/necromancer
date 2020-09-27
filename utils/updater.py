from datetime import datetime
import discord
from discord.ext import commands

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Checks
	def is_admin():
		async def predicate(ctx):
			member = ctx.author
			return member.guild_permissions.administrator or member.guild_permissions.manage_channels	
		return commands.check(predicate)

	# Commands
	# Sets the game channel
	@commands.command(
		name="setchannel",
		help="Sets the text channel to play Thread Necromancy on. You can only have one channel per server.",
		brief="Set the server's TNG channel"
	)
	@is_admin()
	async def setchannel(self, ctx, channel: discord.TextChannel):
		database = self.bot.get_cog("Database")
		database.add_server(ctx.guild.id, channel.id)
		await ctx.send(f"Successfully set <#{channel.id}> as a necromancy channel for this server.")

	@setchannel.error
	async def setchannel_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper channel!")


	# Forces the leaderboard to update
	@commands.command(
		name="update",
		help="Forces the bot to update the TNG leaderboard. Should always be after a bot restart.",
		brief="Forces the leaderbard to update."
	)
	@is_admin()
	async def update(self, ctx):
		database, guild = self.bot.get_cog("Database"), ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		first = True
		async for message in channel.history(limit=None, oldest_first=True):
			if first:
				# TBD
				print("this is the first message")
			else:
				# TBD
				print("this is not the first message")

	@update.error
	async def update_error(self, ctx, error):
		if isinstance(error, TypeError):
			await ctx.send("This guild does not have a game channel!")

def setup(bot):
    bot.add_cog(Updater(bot))