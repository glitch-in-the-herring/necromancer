import discord
from discord.ext import commands

class Leaderboard():
	pass

def setup(bot):
    bot.add_cog(Leaderboard(bot))
