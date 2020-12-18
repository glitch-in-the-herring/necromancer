from discord.ext import Commands
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


	@bot.group(
		name="toggle",
		short_doc="Toggles between game modes. Available modes are 'normal' and 'quadratic'",
	)
	@is_admin
	async def toggle(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid toggle')


	@toggle.command(
		name="normal",
		help="Changes the score counting mode to normal. Scores are calculated using linear differences of timestamps.",
		brief="Changes the score counting mode to normal."
	)		
	async def normal(self, ctx):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		mode = database.retrieve_guild_mode(guild.id)
		if mode != 1:
			database.update_mode(guild.id, 1)
			database.commit()
			await ctx.send("Gamemode has been set to normal.")
			await channel.send("Gamemode has been set to normal.")


	@toggle.command(
		name="quadratic",
		help="Changes the score counting mode to quadratic. Scores are calculated based on the square of the difference of timesamps.",
		brief="Changes the score counting mode to quadratic."
	)		
	async def quadratic(self, ctx):
		guild = ctx.guild
		channel = guild.get_channel(database.retrieve_channel(guild.id))
		mode = database.retrieve_guild_mode(guild.id)
		if mode != 2:
			database.update_mode(guild.id, 2)
			database.commit()
			await ctx.send("Gamemode has been set to quadratic.")
			await channel.send("Gamemode has been set to quadratic.")

def setup(bot):
	bot.add_cog(Mode(bot))
