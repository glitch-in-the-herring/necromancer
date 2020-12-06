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
		if len(args) == 0:
			guild_scores = list(database.retrieve_guild_scores(guild.id))
			own_score = database.retrieve_score(guild.id, author.id)
			own_count = database.retrieve_count(guild.id, author.id)
			hms_score = converter.secs_to_hms(own_score)
			hms_average = converter.secs_to_hms(own_score / own_count)
			rank = guild_scores.index((own_score,)) + 1
			leaderboard_embed = discord.Embed(title=num2words(rank, to="ordinal_num") + f" Place: {author.name}#{author.discriminator}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
			leaderboard_embed.add_field(
				name=":stopwatch: Score",
				value=f"{hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
				inline=False
			)
			leaderboard_embed.add_field(
				name=":abacus: Average score",
				value=f"{hms_average[0]:02}:{hms_average[1]:02}:{hms_average[2]:02}",
				inline=False
			)			
		elif len(args) == 1:
			try:
				top10 = list(database.retrieve_top_ten(guild.id))
				upto, i = int(args[0]), 0
				leaderboard_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
				while i < upto:
					member = guild.get_member(top10[i][0])
					hms_score = converter.secs_to_hms(top10[i][1])
					if member is not None:
						leaderboard_embed.add_field(
							name=num2words(i+1, to="ordinal_num") + " Place:",
							value=guild.get_member(top10[i][0]).name + "#" + str(guild.get_member(top10[i][0]).discriminator) + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
							inline=False	
						)
					else:
						leaderboard_embed.add_field(
							name=num2words(i+1, to="ordinal_num") + " Place:",
							value="User not found" + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
							inline=False	
						)
					i += 1
		await ctx.send(embed=leaderboard_embed)		
			except ValueError:
				await ctx.send("Not a Number!")

def setup(bot):
	bot.add_cog(Leaderboard(bot))
