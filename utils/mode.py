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
		name="toggle",
		help="Toggles between game modes. Available modes are 'normal' (1) and 'quadratic' (2)",
		brief="Toggles between game modes"
	)
	@is_admin()
	async def toggle(self, ctx, mode):
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
				database.update_mode(guild.id, 1)
				database.commit()
				await ctx.send("Gamemode has been set to normal.")
				await channel.send("Gamemode has been set to normal.")

	@toggle.error
	async def toggle_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please specify a proper game mode!")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have permissions to execute this command!")
		else:
			await ctx.send(error)

def setup(bot):
	bot.add_cog(Mode(bot))
