from datetime import datetime
import discord
from discord.ext import commands

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Checks
	# Checks if the user invoking the command is an admin
	def is_admin():
		async def predicate(ctx):
			member = ctx.author
			return member.guild_permissions.administrator or member.guild_permissions.manage_channels	
		return commands.check(predicate)


	# Listeners
	# Listens for new messages in the game channel
	@commands.Cog.listener()
	async def on_message(self, message):
		database, converter = self.bot.get_cog("Database"), self.bot.get_cog("Converter")
		guild, author = message.guild, message.author
		channel = database.retrieve_channel(guild.id)
		if message.channel == channel:
			previous_message = await channel.fetch_message(database.retrieve_last_message(guild.id))
			if previous_message.author != author:
				score_delta = message.created_at - previous_message.created_at
				score = converter.delta_to_secs(score_delta) + database.retrieve_score(guild.id, author.id)
				database.update_score(guild.id, current_author, score, 0)
				database.update_server(guild.id, channel.id, message.id)
			else:
				await message.delete()


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
		database.update_server(ctx.guild.id, channel.id, channel.last_message_id)
		database.commit()
		await ctx.send(f"Successfully set <#{channel.id}> as a necromancy channel for this server.")

	@setchannel.error
	async def setchannel_error(self, ctx, error):
		print(error)
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper channel!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")


	# Forces the leaderboard to update
	@commands.command(
		name="update",
		help="Forces the bot to update the TNG leaderboard. Should always be after a bot restart.",
		brief="Forces the leaderbard to update."
	)
	@is_admin()
	async def update(self, ctx):
		guild = ctx.guild
		database, converter = self.bot.get_cog("Database"), self.bot.get_cog("Converter")
		channel =  guild.get_channel(database.retrieve_channel(guild.id))
		first = True
		async for message in channel.history(limit=None, oldest_first=True):
			if first:
				current_timestamp = message.created_at
				current_author = message.author.id
				first = False
				database.update_score(guild.id, current_author, 0, 0)
			else:
				previous_author, current_author = current_author, message.author.id
				if previous_author != current_author:
					previous_timestamp, current_timestamp = current_timestamp, message.created_at
					score_delta = current_timestamp - previous_timestamp
					score = converter.delta_to_secs(score_delta) + database.retrieve_score(guild.id, current_author)
					database.update_score(guild.id, current_author, score, 0)

		database.update_server(guild.id, channel.id, channel.last_message_id)		
		database.commit()
		await ctx.send("Successfully updated the channel.")

	@update.error
	async def update_error(self, ctx, error):
		print(error)
		if isinstance(error, TypeError):
			await ctx.send("This guild does not have a game channel!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")


def setup(bot):
    bot.add_cog(Updater(bot))
