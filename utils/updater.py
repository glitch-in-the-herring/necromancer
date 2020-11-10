import logging
from datetime import datetime
import discord
from discord.ext import commands
import utils.database as database
import utils.converter as converter
from main import config

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Checks
	# Checks if the user invoking the command is an admin
	# Currently hardcoded
	def is_admin():
		async def predicate(ctx):
			member = ctx.author
			return member.id in [int(config["sysadmin_id"])]	
		return commands.check(predicate)


	# Listeners
	# Listens for new messages in the game channel
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author != self.bot.user:
			guild, author, created_at = message.guild, message.author, message.created_at
			channel = guild.get_channel(database.retrieve_channel(guild.id))
			if channel != None and channel == message.channel:
				try:
					previous_author, previous_timestamp = database.retrieve_last_message(guild.id)
					if previous_author != author.id:
						score_delta = created_at - datetime.strptime(previous_timestamp, "%Y-%m-%d %H:%M:%S")
						score_increase = converter.delta_to_secs(score_delta)
						score = score_increase + database.retrieve_score(guild.id, author.id)
						database.update_score(guild.id, author.id, score)
						database.update_last_message(guild.id, author.id, created_at.strftime("%Y-%m-%d %H:%M:%S"))
						database.commit()
					else:
						await message.delete()
				except TypeError:				
					database.update_last_message(guild.id, author.id, created_at.strftime("%Y-%m-%d %H:%M:%S"))

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		guild, author, created_at = message.guild, message.author, message.created_at
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		if channel != None and channel == message.channel:
			await message.channel.send(f"{message.author.mention} deleted a message.")

	# Commands
	# Sets the game channel
	@commands.command(
		name="setchannel",
		help="Sets the text channel to play Thread Necromancy on. You can only have one channel per server.",
		brief="Set the server's TNG channel."
	)
	@is_admin()
	async def setchannel(self, ctx, channel: discord.TextChannel):
		database.update_server(ctx.guild.id, channel.id)
		database.commit()
		await ctx.send(f"Successfully set <#{channel.id}> as the necromancy channel for this server.")
		logging.info(f'[{datetime.now()}] CHANNEL on server: {ctx.guild.id}, new channel: {channel.id}')

	@setchannel.error
	async def setchannel_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper channel!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			print(error)


	# Forces the leaderboard to update
	@commands.command(
		name="update",
		help="Forces the bot to update the TNG leaderboard. Should always be after a bot restart.",
		brief="Forces the leaderbard to update."
	)
	@is_admin()
	async def update(self, ctx):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		first = True
		database.clear_score(guild.id)
		async for message in channel.history(limit=None, oldest_first=True):
			if first:
				current_timestamp = message.created_at
				current_author = message.author.id
				first = False
				database.update_score(guild.id, current_author, 0)
				database.update_last_message(guild.id, current_author, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
			else:
				previous_author, current_author = current_author, message.author.id
				if previous_author != current_author:
					previous_timestamp, current_timestamp = current_timestamp, message.created_at
					score_delta = current_timestamp - previous_timestamp
					score_increase = converter.delta_to_secs(score_delta)
					score = score_increase + database.retrieve_score(guild.id, current_author)
					if current_author != self.bot.user.id:
						database.update_score(guild.id, current_author, score)
						database.update_last_message(guild.id, current_author, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
					else:
						database.update_last_message(guild.id, 0, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
					
		database.commit()
		await ctx.send("Successfully updated the channel.")
		logging.info(f'[{datetime.now()}] UPDATE on server: {guild.id}')

	@update.error
	async def update_error(self, ctx, error):
		if isinstance(error, TypeError):
			await ctx.send("This guild does not have a game channel!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			print(error)

def setup(bot):
	bot.add_cog(Updater(bot))
