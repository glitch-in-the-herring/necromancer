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
			return member.id in [int(config["sysadmin_id"])]	
		return commands.check(predicate)


	@commands.command(
		name="gm",
		help="Changes gamemodes. Available modes are 'normal' (1) and 'quadratic' (2)",
		brief="Changes gamemodes"
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
			if mode == 2:
				database.update_mode(guild.id, 2)
				database.commit()
				await ctx.send("Gamemode has been set to quadratic.")
				await channel.send("Gamemode has been set to quadratic.")
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

def setup(bot):
	bot.add_cog(Mode(bot))
