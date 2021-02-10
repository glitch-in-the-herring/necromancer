import discord
from discord.ext import commands

class About(commands.Cog):
	def __init__ (self, bot):
		self.bot = bot

	@commands.command(
		name="about"
	)
	async def about(self, ctx):
		embed = discord.Embed(
			title="About me", 
			colour=discord.Colour(0xdad7a0), 
			description="Developed by red herring#5078. [check out the source code](https://github.com/glitch-in-the-herring/necromancer)"
		)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(About(bot))
