from datetime import datetime, timezone
import discord
from discord.ext import commands
from num2words import num2words

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
		database, converter = self.bot.get_cog("Database"), self.bot.get_cog("Converter")
		try:
			top10 = list(database.retrieve_top_ten(guild.id))
			if len(args) == 0:
				top10_scores = [x[1] for x in top10]
				own_score = database.retrieve_score(guild.id, author.id)
				hms_score = converter.secs_to_hms(own_score)
				rank = top10_scores.index(own_score) + 1
				leaderboard_embed = discord.Embed(title=num2words(rank, to="ordinal_num") + f" Place: {author.mention}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
				leaderboard_embed.add_field(
					name=":stopwatch: Score",
					value=f"{hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}"
				)
			elif len(args) == 1:
				upto, i = int(args[0]), 0
				leaderboard_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
				while i < upto:
					print("current i:" + str(i))
					hms_score = converter.secs_to_hms(top10[i][1])
					leaderboard_embed.add_field(
						name=num2words(i+1, to="ordinal_num") + " Place:",
						value=f"{guild.get_member(top10[i][0]).name}#{guild.get_member(top10[i][0]).discriminator}: {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
						inline=false
					)
					i += 1
			await ctx.send(embed=leaderboard_embed)
		except TypeError:
			await ctx.send("Nobody has played yet!")


def setup(bot):
	bot.add_cog(Leaderboard(bot))
