import discord
from discord.ext import commands

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		name="setchannel",
		help="Sets the text channel to play Thread Necromancy on. You can only have one channel per server.",
		brief="Set the server's TNG channel"
	)
	async def setchannel(self, ctx, channel: discord.TextChannel):
		database = self.bot.get_cog("Database")
		database.add_server(ctx.guild.id, channel.id)
		await ctx.send(f"Successfully set <#{channel.id}> as a necromancy channel for this server.")

	@commands.command(
		name="update",
		help="Forces the bot to update the TNG leaderboard. Should always be after a bot restart.",
		brief="Forces the leaderbard to update."
	)
	async def update(self, ctx):
		database, guild = self.bot.get_cog("Database"), ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		print(channel.id)


def setup(bot):
    bot.add_cog(Updater(bot))