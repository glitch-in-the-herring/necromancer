import asyncio
import logging
import timeit
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
	def is_admin():
		async def predicate(ctx):
			member = ctx.author
			permission = discord.Permissions()
			return member.id in [int(config["sysadmin_id"])] or member.guild_permissions.manage_channels
		return commands.check(predicate)


	# Listeners
	# Listens for new messages in the game channel
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author != self.bot.user:
			guild, author, created_at = (
				message.guild, 
				message.author, 
				message.created_at
			)
			channel = guild.get_channel(database.retrieve_channel(guild.id))
			if channel is not None and channel == message.channel:
				try:
					gamemode = database.retrieve_guild_mode(guild.id)
					previous_author, previous_timestamp = database.retrieve_last_message(guild.id)
					if previous_author != author.id:
						score_delta = created_at - datetime.strptime(previous_timestamp, "%Y-%m-%d %H:%M:%S")
						if gamemode == 1:
							score_increase = converter.delta_to_secs(score_delta)
						elif gamemode == 2:
							score_increase = converter.delta_to_secs(score_delta) ** 2						
						score = score_increase + database.retrieve_score(guild.id, author.id)
						count = database.retrieve_count(guild.id, author.id) + 1
						database.update_score(guild.id, author.id, score, count)
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
		if channel is not None and channel == message.channel:
			await message.channel.send(f"{message.author.mention} deleted a message.")

	# Commands
	# Sets the game channel
	@commands.command(
		name="setchannel",
		help="Sets the text channel to play Thread Necromancy on. You can only have one channel per server.",
		brief="Set the server's TNG channel."
	)
	@is_admin()
	async def setchannel(self, ctx, channel:discord.TextChannel):
		database.update_server(ctx.guild.id, channel.id, 1, 0)
		database.commit()
		await ctx.send(f"Successfully set <#{channel.id}> as the necromancy channel for this server.")
		logging.info(f'CHANNEL on server: {ctx.guild.id}, new channel: {channel.id}')

	@setchannel.error
	async def setchannel_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper channel!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			await ctx.send(error)


	# Forces the leaderboard to update
	@commands.command(
		name="update",
		help="Forces the bot to update the leaderboard. Should always be done after a bot restart.",
		brief="Forces the leaderbard to update."
	)
	@is_admin()
	async def update(self, ctx):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		first, gamemode = True, 1
		counting = database.retrieve_guild_counting(guild.id)
		database.clear_score(guild.id)
		async for message in channel.history(limit=None, oldest_first=True):
			if first:
				first = False
				current_timestamp = message.created_at
				current_author = message.author.id
				database.update_score(guild.id, current_author, 0, 1)
				database.update_last_message(guild.id, current_author, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
			else:
				previous_author, current_author = current_author, message.author.id
				if previous_author != current_author and current_author != self.bot.user.id:
					previous_timestamp, current_timestamp = (
						current_timestamp, 
						message.created_at
					)
					score_delta = current_timestamp - previous_timestamp
					if counting == 0: 	
						if gamemode == 1:
							score_increase = converter.delta_to_secs(score_delta)
						elif gamemode == 2:
							score_increase = converter.delta_to_secs(score_delta) ** 2
					elif counting == 1:
						score_increase = converter.delta_to_secs(score_delta)
					elif counting == 2:
						score_increase = converter.delta_to_secs(score_delta) ** 2
					score = score_increase + database.retrieve_score(guild.id, current_author)
					count = database.retrieve_count(guild.id, current_author) + 1
					database.update_score(guild.id, current_author, score, count)
					database.update_last_message(guild.id, current_author, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
				elif current_author == self.bot.user.id:
					if message.content == "Gamemode has been set to normal." and counting == 0:
						gamemode = 1
					elif message.content == "Gamemode has been set to quadratic." and counting == 0:
						gamemode = 2
					elif message.content.startswith("Timer has been reset to zero."):
						current_timestamp = message.created_at
						current_author = previous_author
						database.update_last_message(guild.id, previous_author, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
					else:
						database.update_last_message(guild.id, 0, current_timestamp.strftime("%Y-%m-%d %H:%M:%S"))

		database.commit()
		await ctx.send("Done")
		logging.info(f'UPDATE on server: {guild.id}')

	@update.error
	async def update_error(self, ctx, error):
		if isinstance(error, AttributeError):
			await ctx.send("This guild does not have a game channel!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			await ctx.send(error)


	@commands.command(
		name="clear",
		help="Deletes the entire scoreboard in a server. Useful for diagnosing errors.",
		brief="Deletes the entire scoreboard."
	)
	@is_admin()
	async def clear(self, ctx):
		database.clear_score(ctx.guild.id)
		await ctx.send("Deleted the guild's score")
		logging.info(f'CLEAR on server: {ctx.guild.id}')

	@commands.command(
		name="purge",
		help="Deletes messages up to some point in the game channel.",
		brief="Deletes messages."
	)
	@is_admin()
	async def purge(self, ctx, count:int, reason:str):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		await channel.purge(limit=count)
		await channel.send(f"Timer has been reset to zero. Reason: {reason}")
		logging.info(f'PURGE on server: {ctx.guild.id}, count: {count}, reason: {reason}')


	@commands.command(
		name="purgeall",
		help="Deletes all the messages in the game channel.",
		brief="Deletes everything it touches."
	)
	@is_admin()
	async def purgeall(self, ctx, reason:str):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		await channel.purge()
		await channel.send(f"Timer has been reset to zero. Reason: {reason}")
		logging.info(f'PURGE on server: {ctx.guild.id}, reason: {reason}')					


def setup(bot):
	bot.add_cog(Updater(bot))
