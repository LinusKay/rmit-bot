import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.rmit')

@bot.event
async def on_ready():
	print('online')
	await bot.change_presence(activity=discord.Game(name="yay!"))
	
#run bot
bot.run("NzE1MTEwOTQ0MTk1MzQ2NDg2.Xs4d2A.wocePR9Gj_xwjiuiG2pLDUkKxlw")