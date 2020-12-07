from datetime import datetime, timezone
import math
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
		name="top",
		help="Shows the leaderboard. Still hardcoded to only show the top 10 players.",
		brief="Shows the leaderboard. Up to 10 players may be displayed."
	)
	async def top(self, ctx):
		guild, author = ctx.guild, ctx.author
		server_board = list(database.retrieve_server_board(guild.id))
		leaderboard_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
		print(guild.icon)
		leaderboard_embed.set_thumbnail(guild.icon)
		pages = math.floor(len(server_board)/5)
		leaderboard_embed.set_footer(text=f"Page 1 of {pages}")
		for y, x in enumerate(server_board[0:5]):
			member = guild.get_member(x[0])
			hms_score = converter.secs_to_hms(x[1])
			if member is not None:
				leaderboard_embed.add_field(
					name=num2words(y+1, to="ordinal_num") + " Place:",
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
		leaderboard_message = await ctx.send(embed=leaderboard_embed)
		await leaderboard_message.add_reaction(":arrow_left:")
		await leaderboard_message.add_reaction(":arrow_right:")


def setup(bot):
	bot.add_cog(Leaderboard(bot))
