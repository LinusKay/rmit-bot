import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

static_maps_API_key = 'AIzaSyA6vEH85dgBFj-cuPW38lTXFsY84c-duxk'

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

@bot.command(aliases=['addcourse'])
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

@bot.command(aliases=['removecourse'])
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

@bot.command(aliases=['linkme'])
async def links(ctx, *, arg=None):
	with open('data/links.csv') as f:
		links = f.read().splitlines()
		if arg is None:
			all_links = ''
			for link in links:
				link_data = link.split(',')
				link_title = link_data[0]
				all_links = all_links + link_title + '\n'
			links_embed = discord.Embed(
				title = 'RMIT Links',
				description = 'All available link shortcuts. type .rmit links <link name>',
				colour = 0xE00303
				)
			links_embed.add_field(name='Links', value=all_links)
			links_embed.set_footer(text='All links sourced from RMIT official website https://rmit.edu.au', icon_url='https://libus.xyz/i/0d0daddd526317b5a5c647e32c71180d/upload.png')
			await ctx.send(embed=links_embed)
			
		else:
			for link in links:
				link_data = link.split(',')
				link_title = link_data[0]
				link_text_1 = ''
				link_text_2 = ''
				if arg.lower() == link_title.lower():
					link_description = link_data[1]
					if len(link_data) > 2:
						link_text_1 = bytes(str(link_data[2]), "utf-8").decode("unicode_escape")
					else:
						link_text_1 = ''
					if len(link_data) > 3:
						link_text_2 = bytes(str(link_data[3]), "utf-8").decode("unicode_escape")
					else:
						link_text_2 = ''
						
					links_embed = discord.Embed(
						title = 'RMIT Links',
						description = link_title + ' - ' + link_description,
						colour = 0xE00303
						)
					if link_text_1 != '':
						links_embed.add_field(name=link_title, value=link_text_1)
					if link_text_2 != '':
						links_embed.add_field(name=link_title, value=link_text_2)
					links_embed.set_footer(text='All links sourced from RMIT official website https://rmit.edu.au', icon_url='https://libus.xyz/i/0d0daddd526317b5a5c647e32c71180d/upload.png')
					await ctx.send(embed=links_embed)

@bot.command(aliases=['findbuilding'])
async def building(ctx, arg=None):
	with open('data/buildings.csv') as f:
		buildings = f.read().splitlines()
		if arg is None:
			melbourne_buildings = ''
			bundoora_buildings = ''
			brunswick_buildings = ''
			for building in buildings:
				building_data = building.split(',')
				building_name = building_data[1]
				building_campus = building_data[3]
				if building_campus == 'Melbourne City Campus':
					melbourne_buildings = melbourne_buildings + building_name + ', '
				elif building_campus == 'Bundoora Campus':
					bundoora_buildings = bundoora_buildings + building_name + ', '
				elif building_campus == 'Brunswick Campus':
					brunswick_buildings = brunswick_buildings + building_name + ', '
			await ctx.send('**Melbourne City Campus**\n' + melbourne_buildings)
			await ctx.send('**Bundoora Campus**\n' + bundoora_buildings)
			await ctx.send('**Brunswick Campus**\n' + brunswick_buildings)
		else:
			for building in buildings:
				if building.startswith(arg + ','):
					building_data = building.split(',')
					building_num = building_data[0]
					building_name = building_data[1]
					building_address = building_data[2]
					building_campus = building_data[3]
					parse_url = building_address.replace(' ', '+')
					parse_map = building_campus.lower().replace(' ', '-')
					building_embed = discord.Embed(
						title = 'Find an RMIT building',
						description = '[' + building_name + '](https://www.rmit.edu.au/maps/melbourne-city-campus/building-' + building_num + '), ' + building_campus,
						colour = 0xE00303
						)
					building_embed.add_field(name='Address', value=building_address + '\n[Get directions](https://www.google.com/maps?f=d&daddr=' + parse_url + ')\n[Download Campus Map](https://www.rmit.edu.au/content/dam/rmit/documents/maps/pdf-maps/rmit-' + parse_map + '-map.pdf)')
					building_embed.set_image(url='https://maps.googleapis.com/maps/api/staticmap?center=' + parse_url + '&markers=' + parse_url + '&zoom=16&size=400x400&key=AIzaSyA6vEH85dgBFj-cuPW38lTXFsY84c-duxk')
					await ctx.send(embed=building_embed)
					
@bot.command()
async def ping(ctx):
	await ctx.send(str(ctx.created_at))
	
@bot.command()
async def help(ctx):
	help_embed = discord.Embed(
		title = 'RMIT Bot Commands',
		description = 'Find out what I can do!',
		colour = 0xE00303
		)
	help_embed.add_field(name='.rmit findbuilding [building number]', value='Find a specific RMIT building. Not including a parameter will display all buildings. Also try: findbuilding/building', inline=False)
	help_embed.add_field(name='.rmit links [building number]', value='Browse a selection of shortcuts to RMIT services. Not including a parameter will display all available links.', inline=False)
	help_embed.set_footer(text = 'This bot was created by Linus Kay (libus#5949) and is by no means officially endorsed by RMIT')
	await ctx.send(embed=help_embed)

#run bot
bot.run("NzE1MTEwOTQ0MTk1MzQ2NDg2.Xs4d2A.wocePR9Gj_xwjiuiG2pLDUkKxlw")