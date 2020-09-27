import json
from discord.ext import commands

with open("config.json") as f:
	config = json.load(f)

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

def setup(bot):
    bot.add_cog(Config(bot))