from datetime import datetime, timezone
import logging
import math
import discord
from discord.ext import commands
from num2words import num2words
import utils.database as database
import utils.converter as converter
from main import config

class Leaderboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Listeners
	# Listens for reactions to leaderboard messages
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		message = reaction.message
		if message.author == self.bot.user and user != self.bot.user:
			guild = message.guild
			old_embed = message.embeds[0]
			if old_embed.title == f"Server rank for {guild.name}":
				old_page = int(old_embed.footer.text.split()[1])
				server_board = list(enumerate(database.retrieve_server_board(guild.id)))
				pages = math.floor(len(server_board)/5)
				new_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
				new_embed.set_thumbnail(url=str(guild.icon_url))			
				if str(reaction) == "⬅️" and old_page > 1:
					page = old_page - 1
					await message.clear_reactions()
				elif str(reaction) == "➡️" and old_page < pages:
					page = old_page + 1
					await message.clear_reactions()
				else:
					return
				new_embed.set_footer(text=f"Page {page} of {pages}")
				for y, x in server_board[(5 * (page-1)):(5 * (page))]:
					nth_member = guild.get_member(x[0])
					hms_score = converter.secs_to_hms(x[1])
					if nth_member is not None:
						new_embed.add_field(
							name=num2words(y+1, to="ordinal_num") + " Place:",
							value= str(nth_member) + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
							inline=False	
						)
					else:
						new_embed.add_field(
							name=num2words(i+1, to="ordinal_num") + " Place:",
							value="User not found" + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
							inline=False	
						)
				await message.edit(embed=new_embed)
				if page > 1:
					await message.add_reaction("⬅️")
				if page < pages:
					await message.add_reaction("➡️")

	# Commands
	# Retrieves the server leaderboard
	@commands.command(
		name="top",
		help="Shows the leaderboard. Use arrow reactions to navigate",
		brief="Shows the leaderboard."
	)
	async def top(self, ctx, page:int=1):
		guild, author = ctx.guild, ctx.author
		server_board = list(enumerate(database.retrieve_server_board(guild.id)))
		if len(server_board)/5 < 0:
			pages = 1
		else:
			pages = math.floor(len(server_board)/5)
		if page <= pages and page >= 1:
			leaderboard_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
			leaderboard_embed.set_thumbnail(url=str(guild.icon_url))
			leaderboard_embed.set_footer(text=f"Page {page} of {pages}")
			for y, x in server_board[(5 * (page-1)):(5 * (page))]:
				nth_member = guild.get_member(x[0])
				hms_score = converter.secs_to_hms(x[1])
				if nth_member is not None:
					leaderboard_embed.add_field(
						name=num2words(y+1, to="ordinal_num") + " Place:",
						value= str(nth_member) + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
						inline=False	
					)
				else:
					leaderboard_embed.add_field(
						name=num2words(i+1, to="ordinal_num") + " Place:",
						value="User not found" + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
						inline=False	
					)
			leaderboard_message = await ctx.send(embed=leaderboard_embed)
			if page > 1:
				await leaderboard_message.add_reaction("⬅️")
			if page < pages:
				await leaderboard_message.add_reaction("➡️")
		else:
			nothing_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
			nothing_embed.add_field(
				name="404",
				value="Not found",
				inline=False	
			)			
			await ctx.send(embed=nothing_embed)


	# Retrieves the personal stats
	@commands.command(
		name="rank",
		help="Shows the personal stats.",
		brief="Shows the personal stats."
	)
	async def rank(self, ctx, user:discord.Member=None):
		if user is None:
			user = ctx.author
		guild = ctx.guild
		server_board = list(database.retrieve_server_board(guild.id))
		score = database.retrieve_score(guild.id, user.id)
		count = database.retrieve_count(guild.id, user.id)
		hms_score = converter.secs_to_hms(score)
		hms_average = converter.secs_to_hms(round(score/count))
		rank = server_board.index((user.id, score)) + 1
		leaderboard_embed = discord.Embed(title=num2words(rank, to="ordinal_num") + f" Place: {str(user)}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
		leaderboard_embed.set_thumbnail(url=str(user.avatar_url))
		leaderboard_embed.set_footer(text=f"{count} posts")
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
		await ctx.send(embed=leaderboard_embed)

	@rank.error
	async def rank_error(self, ctx, error):
		if isinstance(error, discord.ext.commands.errors.MemberNotFound):
			await ctx.send("User not found in this guild.")
		elif isinstance(error, ZeroDivisionError):
			await ctx.send("User not found.")
		else:
			await ctx.send(f"Unknown error occured")
			logging.error(error)

def setup(bot):
	bot.add_cog(Leaderboard(bot))
