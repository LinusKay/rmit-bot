import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.rmit ')
bot.remove_command("help")

@bot.event
async def on_ready():
	print('online')
	await bot.change_presence(activity=discord.Game(name="yay!"))
	
@bot.command()
async def createcourse(ctx, *, arg):
	guild = ctx.message.guild
	category = await guild.create_category(arg)
	words = category.name.split()
	letters = [word[0] for word in words]
	category_abbrev = "".join(letters)
	await guild.create_text_channel(category_abbrev + '-general', category=category)
	await guild.create_text_channel(category_abbrev + '-assignments', category=category)
	await guild.create_text_channel(category_abbrev + '-lectures', category=category)
	course_role = await guild.create_role(name=category.name)
	await category.set_permissions(guild.default_role, read_messages=False)
	await category.set_permissions(course_role, read_messages=True, send_messages=True)
	await ctx.send('Created course`' + category.name + '`')

@bot.command()
async def deletecourse(ctx, cat_id, delete_role=None):
	guild = ctx.message.guild
	categories = guild.categories
	for category in categories:
		if category.id == int(cat_id):
			await ctx.send("Deleted course `" + category.name + '`')
			text_channels = category.channels
			text_channels = category.channels
			for channel in text_channels:
				await channel.delete()
			await category.delete()
			if delete_role != None:
				roles = guild.roles
				for role in roles:
					if role.name == category.name:
						await ctx.send("Deleted role `" + role.name + '`')
						await role.delete()

@bot.command()
@has_permissions(administrator=True)
async def help(ctx):
	help_embed = discord.Embed(
		title = 'Help',
		description = 'How to use the RMIT Bot',
		colour = 0xE00303
		)
	await ctx.send(embed=help_embed)

#run bot
bot.run("NzE1MTEwOTQ0MTk1MzQ2NDg2.Xs4d2A.wocePR9Gj_xwjiuiG2pLDUkKxlw")