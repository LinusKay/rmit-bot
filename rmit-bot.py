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
	category = await guild.create_category(arg)
	words = category.name.split()
	letters = [word[0] for word in words]
	category_abbrev = "".join(letters)
	await guild.create_text_channel(category_abbrev + '-general', category=category)
	await guild.create_text_channel(category_abbrev + '-assignments', category=category)
	await guild.create_text_channel(category_abbrev + '-lectures', category=category)
	course_role = await guild.create_role(name=category.name)
	await cat.set_permissions(guild.default_role, read_messages=False)
	await cat.set_permissions(course_role, read_messages=True, send_messages=True)
	
#run bot
bot.run("NzE1MTEwOTQ0MTk1MzQ2NDg2.Xs4d2A.wocePR9Gj_xwjiuiG2pLDUkKxlw")