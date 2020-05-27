import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.rmit ')

@bot.event
async def on_ready():
	print('online')
	await bot.change_presence(activity=discord.Game(name="yay!"))
	
@bot.command()
async def copyme(ctx, *, arg):
	await ctx.send(arg)
	
@bot.command()
async def createclass(ctx, *, arg):
	guild = ctx.message.guild
	cat = await guild.create_category(arg)
	words = cat.name.split()
	letters = [word[0] for word in words]
	cat_name_short = "".join(letters)
	await guild.create_text_channel(cat_name_short + '-general', category=cat)
	await guild.create_text_channel(cat_name_short + '-assignments', category=cat)
	await guild.create_text_channel(cat_name_short + '-lectures', category=cat)
	role = await guild.create_role(name=cat.name)
	await cat.set_permissions(role, send_messages=True)
	
#run bot
bot.run("NzE1MTEwOTQ0MTk1MzQ2NDg2.Xs4d2A.wocePR9Gj_xwjiuiG2pLDUkKxlw")