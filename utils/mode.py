import logging
import discord
from discord.ext import commands
import utils.database as database
from main import config

class Mode(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	
	# Checks
	# Checks if the user invoking the command is an admin
	def is_admin():
		async def predicate(ctx):
			member = ctx.author
			permission = discord.Permissions()
			return member.id in [int(config["sysadmin_id"])] or member.guild_permissions >= permission.manage_channels
		return commands.check(predicate)


	@commands.command(
		name="gm",
		help="Changes gamemode. Available modes are 'normal' (1) and 'quadratic' (2)",
		brief="Changes gamemode."
	)
	@is_admin()
	async def gm(self, ctx, mode:int):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		current_mode = database.retrieve_guild_mode(guild.id)
		if current_mode != mode:
			if mode == 1:
				database.update_mode(guild.id, 1)
				database.commit()
				await ctx.send("Gamemode has been set to normal.")
				await channel.send("Gamemode has been set to normal.")
				logging.info(f'GAMEMODE on server: {ctx.guild.id} to 1')
			if mode == 2:
				database.update_mode(guild.id, 2)
				database.commit()
				await ctx.send("Gamemode has been set to quadratic.")
				await channel.send("Gamemode has been set to quadratic.")
				logging.info(f'GAMEMODE on server: {ctx.guild.id} to 2')				
		else:
			await ctx.send("The current gamemode is already the same")

	@gm.error
	async def gm_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper game mode!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			await ctx.send(error)


	@commands.command(
		name="cm",
		help="Changes the counting mode used when updating the score table. 0 means that the scores are counted based on whatever gamemode was used at the time of posting. 1 means that the scores are counted using normal counting only. 2 means that the scores are counted using the quadratic mode only",
		brief="Changes the counting mode."
	)
	@is_admin()
	async def cm(self, ctx, mode:int = 0):
		guild = ctx.guild
		if mode == 0:
			database.update_counting(guild.id, 0)
			await ctx.send("Counting set to adaptive")
		elif mode == 1:
			database.update_counting(guild.id, 1)
			await ctx.send("Counting set to normal only")
		elif mode == 2:
			database.update_counting(guild.id, 2)
			await ctx.send("Counting set to quadratic only")
		else:
			await ctx.send("Please specify a proper counting mode!")			

	@cm.error
	async def gm_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper counting mode!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			await ctx.send(error)

def setup(bot):
	bot.add_cog(Mode(bot))
