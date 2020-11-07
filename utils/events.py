from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Listeners
	@commands.Cog.listener()
	async def on_ready(self):
		print("We have logged in")
		await self.bot.change_presence(activity=discord.Game(name=f"{prefix}help for info"))


def setup(bot):
    bot.add_cog(Events(bot))
    