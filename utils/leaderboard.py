from datetime import datetime, timezone
import discord
from discord.ext import commands
from num2words import num2words
import utils.database as database
import utils.converter as converter

class Leaderboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Commands
	# Retrieves the leaderboard
	@commands.command(
		name="leaderboard",
		help="Shows the leaderboard. Still hardcoded to only show the top 10 players.",
		brief="Shows the leaderboard. Up to 10 players may be displayed."
	)
	async def leaderboard(self, ctx, *args):
		guild, author = ctx.guild, ctx.author
		try:
			if len(args) == 0:
				guild_scores = list(database.retrieve_guild_scores(guild.id))
				own_score = database.retrieve_score(guild.id, author.id)
				hms_score = converter.secs_to_hms(own_score)
				rank = guild_scores.index((own_score,)) + 1
				leaderboard_embed = discord.Embed(title=num2words(rank, to="ordinal_num") + f" Place: {author.name}#{author.discriminator}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
				leaderboard_embed.add_field(
					name=":stopwatch: Score",
					value=f"{hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}"
				)
			elif len(args) == 1:
				await ctx.send("cover yourself")
				top10 = list(database.retrieve_top_ten(guild.id))
				upto, i = int(args[0]), 0
				await ctx.send("in oil")
				leaderboard_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
				await ctx.send("wait for it to rain")
				while i < upto:
					hms_score = converter.secs_to_hms(top10[i][1])
					leaderboard_embed.add_field(
						name=num2words(i+1, to="ordinal_num") + " Place:",
						value=guild.get_member(top10[i][0]).name + "#" + str(guild.get_member(top10[i][0]).discriminator) + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
						inline=False
					)
					i += 1
					await ctx.send("fly away")
			await ctx.send(embed=leaderboard_embed)
			await ctx.send("did that work or did you die from fall damage?")
		except e:
			await ctx.send("oopsy woopsy")
			await ctx.send(e)

	@leaderboard.error
	async def update_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Incorrect argument!")

def setup(bot):
	bot.add_cog(Leaderboard(bot))
