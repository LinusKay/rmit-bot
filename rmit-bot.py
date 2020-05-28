import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix='.rmit ')
bot.remove_command("help")

@bot.event
async def on_ready():
	print('online')
	await bot.change_presence(activity=discord.Game(name=".rmit help"))
	
@bot.event
async def on_member_join(member):
	channel = discord.utils.get(member.guild.channels, name="general")
	welcome_channel = bot.get_channel(684986753659961408)
	await channel.send('**Welcome **' + member.mention + '!\nCheck out ' + welcome_channel.mention + ' to learn about the server and join course groups!')

@bot.command()
@has_permissions(administrator=True)
async def createcourse(ctx, *, arg):
	args = arg.split(',')
	if len(args) > 1:
		course_code = args[1]
	else:
		course_code = ''
	guild = ctx.message.guild
	categories = guild.categories
	category = await guild.create_category(args[0])
	words = category.name.split()
	letters = [word[0] for word in words]
	category_abbrev = "".join(letters)
	text_channel = await guild.create_text_channel(category_abbrev + '-general', category=category)
	await text_channel.edit(topic='Discuss ' + course_code + ' ' + category.name + '!')
	text_channel = await guild.create_text_channel(category_abbrev + '-assignments', category=category)
	await text_channel.edit(topic='Discuss ' + course_code + ' ' + category.name + ' assignments!')
	text_channel = await guild.create_text_channel(category_abbrev + '-lectures', category=category)
	await text_channel.edit(topic='Discuss ' + course_code + ' ' + category.name + ' lectures!')
	course_role = await guild.create_role(name=category.name)
	await category.set_permissions(guild.default_role, read_messages=False)
	await category.set_permissions(course_role, read_messages=True, send_messages=True)
	await ctx.send('Created course `' + category.name + '`')

@bot.command()
@has_permissions(administrator=True)
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
async def archivecourse(ctx, cat_id):
	guild = ctx.message.guild
	categories = guild.categories
	target_category = 0
	archive_category = 0
	match = False
	i = 0
	while(i < len(categories) and match==False):
		if categories[i].name.lower() == 'archives':
			archive_category = categories[i].id
			await ctx.send('archive category found!')
			match = True
		i+=1
	if match==False:
		archive_category = await guild.create_category('archives')
		await archive_category.set_permissions(guild.default_role, read_messages=False)
	for category in categories:
		if category.id == int(cat_id):
			channels = category.channels
			for channel in channels:
				await channel.edit(category=archive_category)
			await category.delete()

@bot.command()
async def linkme(ctx, *, arg):
	if arg.lower() == 'student support':
		await ctx.send('Try this: https://www.rmit.edu.au/students/support-and-facilities/student-support')
		
@bot.command()
async def building(ctx, arg):
	with open('data/buildings.csv') as f:
		buildings = f.readlines()
		for building in buildings:
			if building.startswith(arg):
				building_data = building.split(',')
				building_num = building_data[0]
				building_name = building_data[1]
				building_address = building_data[2]
				building_campus = building_data[3]
				await ctx.send(str(building_num), building_name, building_address, building_campus)
	

@bot.command()
async def help(ctx):
	help_embed = discord.Embed(
		title = 'RMIT Bot Commands',
		description = 'Find out what I can do!',
		colour = 0xE00303
		)
	help_embed.add_field(name='.rmit createcourse <course name>, [course code]', value='Create a private course category with standard channels, and course role.', inline=False)
	help_embed.add_field(name='.rmit deletecourse <category id> [delete role]', value='Delete a course using category ID. Second param will delete the role too.', inline=False)
	help_embed.add_field(name='.rmit archivecourse <category id>', value='Archive a course using category ID. Will place in private Archives category and keep role.', inline=False)
	help_embed.set_footer(text = 'This bot was created by Linus Kay (libus#5949) and is by no means officially endorsed by RMIT')
	await ctx.send(embed=help_embed)

#run bot
bot.run("NzE1MTEwOTQ0MTk1MzQ2NDg2.Xs4d2A.wocePR9Gj_xwjiuiG2pLDUkKxlw")