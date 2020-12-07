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

	# Listeners
	# Listens for reactions to leaderboard messages
	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		message = reaction.message
		print("bye")
		if message.author == self.bot.user and user != self.bot.user:
			print("hi")
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
				print("pale")
				for y, x in server_board[(5 * (page-1)):(5 * (page))]:
					nth_member = guild.get_member(x[0])
					hms_score = converter.secs_to_hms(x[1])
					if nth_member is not None:
						new_embed.add_field(
							name=num2words(y+1, to="ordinal_num") + " Place:",
							value=nth_member.name + "#" + str(nth_member.discriminator) + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
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
					await leaderboard_message.add_reaction("⬅️")
				if page < pages:
					await leaderboard_message.add_reaction("➡️")

	# Commands
	# Retrieves the leaderboard
	@commands.command(
		name="top",
		help="Shows the leaderboard. Still hardcoded to only show the top 10 players.",
		brief="Shows the leaderboard. Up to 10 players may be displayed."
	)
	async def top(self, ctx, page:int=1):
		guild, author = ctx.guild, ctx.author
		server_board = list(enumerate(database.retrieve_server_board(guild.id)))
		pages = math.floor(len(server_board)/5)
		if page <= pages:
			leaderboard_embed = discord.Embed(title=f"Server rank for {guild.name}", timestamp=datetime.now(timezone.utc), color=discord.Colour(0x100000))
			leaderboard_embed.set_thumbnail(url=str(guild.icon_url))
			leaderboard_embed.set_footer(text=f"Page {page} of {pages}")
			for y, x in server_board[(5 * (page-1)):(5 * (page))]:
				nth_member = guild.get_member(x[0])
				hms_score = converter.secs_to_hms(x[1])
				if nth_member is not None:
					leaderboard_embed.add_field(
						name=num2words(y+1, to="ordinal_num") + " Place:",
						value=nth_member.name + "#" + str(nth_member.discriminator) + ":" + f" {hms_score[0]:02}:{hms_score[1]:02}:{hms_score[2]:02}",
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
			await ctx.send("Nothing to see")


def setup(bot):
	bot.add_cog(Leaderboard(bot))
