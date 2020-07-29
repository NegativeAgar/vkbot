import discord
from discord.ext import commands
import asyncio
import random
import time
import os
import sqlite3
import io 
import requests
from PIL import Image, ImageFont, ImageDraw

db = sqlite3.connect('server.db')
sql = db.cursor()



time_string = time.strftime("%A %X")


prefix = "."
bot = commands.Bot(command_prefix=prefix)


# Команда help
bot.remove_command('help')

@bot.event
async def on_ready():
    game = discord.Game("Помощь [.help] ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Бот запущен!")

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        points INT,
        server_id INT
    )""")
    for guild in bot.guilds:
    	for member in guild.members:
    		if sql.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
    			sql.execute(f"INSERT INTO users VALUES ('{member}',{member.id},{0},{guild.id})")
    			db.commit()
    		else:
    			pass
    db.commit()
    print('База данных запущена!')	


# clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count=20):
    author = ctx.message.author
    await ctx.channel.purge(limit=count)
    await ctx.send(embed=discord.Embed(description=f'Чат очистил администратор: {author.mention}'))
    await sleep(3.0)
    await ctx.channel.purge(limit=1)

# Чат бот
@bot.command()
async def sostav(ctx):
        author = ctx.author
        await ctx.send(f" {author.mention}, если ты это написал, значит ты не в составе :)")

@bot.command()
async def points(ctx, member: discord.Member = None):
	if member is None:
		await ctx.send(embed= discord.Embed(description= f"Количество поинтов **{ctx.author}** составляет **{sql.execute('SELECT points FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]} :gem:**",colour=discord.Colour.blue()))
	else:
		await ctx.send(embed= discord.Embed(description= f"Количество поинтов **{member}** составляет **{sql.execute('SELECT points FROM users WHERE id = {}'.format(member.id)).fetchone()[0]} :gem:**",colour=discord.Colour.blue()))
		
@bot.command(aliases= ['+p'])
@commands.has_permissions(administrator=True)
async def __p(ctx, member: discord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f'**{ctx.author}**, укажите пользователя, которому желаете выдать points')
	else:
		if amount is None:
			await ctx.send(f'**{ctx.author}**, укажите количество, которые хотите добавить пользователю')
		elif amount < 1:
			await ctx.send(f"**ctx.author**, укажите сумму больше 1")
		else:
			sql.execute("UPDATE users SET points = points + {} WHERE id = {}".format(amount, member.id))	
			db.commit()

			await ctx.message.add_reaction('✅')

@bot.command(aliases= ['-p'])
@commands.has_permissions(administrator=True)
async def __take(ctx, member:discord.Member = None, amount=None):
	if member is None:
		await ctx.send(f'**{ctx.author}**, укажите пользователя, у которого желаете забрать points')
	else:
		if amount is None:
			await ctx.send(f'**{ctx.author}**, укажите количество, которые хотите забрать')
		elif amount == 'all':
			sql.execute("UPDATE users SET points = {} WHERE id = {}".format(0, member.id))	
			db.commit()	

		elif int(amount) < 1:
			await ctx.send(f"**ctx.author**, укажите сумму больше 1")
		else:
			sql.execute("UPDATE users SET points = points - {} WHERE id = {}".format(int(amount), member.id))	
			db.commit()

			await ctx.message.add_reaction('✅')

@bot.command(aliases= ['leaderboard','lb','top'])
async def __leaderboard(ctx):
	embed= discord.Embed(title = 'Топ 5',colour=discord.Colour.blue())
	counter = 0
	for row in sql.execute("SELECT name,points FROM users WHERE server_id = {} ORDER BY points DESC LIMIT 5".format(ctx.guild.id)):
		counter += 1
		embed.add_field(
			name = f'# {counter} | `{row[0]}`',
			value = f'Points: {row[1]}',inline=False
		)
	await ctx.send(embed=embed)	
# Подключение к каналу

@bot.event
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.guild.roles, id=712600261012488242)
    await member.add_roles(role)

    if sql.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
    	sql.execute(f"INSERT INTO users VALUES ('{member}',{member.id},{0},{member.guild.id}")
    	db.commit()
    else:
    	pass


# commands
@bot.command()
async def help(ctx):
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title="Помощь по боту", colour=discord.Colour.orange())
        emb.add_field(name='Команды:',value='`.info @id` - Посмотреть статистику'
                            '\n`.sostav` - Состав команды!'
                            '\n`.points @id` - посмотреть поинты',inline=False)
        await ctx.send(embed=emb)



# info
@bot.command()
async def info(ctx, member: discord.Member):
    emb = discord.Embed(title="Статистика `{}`".format(member.name), colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.add_field(name='Имя:', value=member.name)
    emb.add_field(name="Зашёл на канал:", value=str(member.joined_at)[:10])
    emb.add_field(name='ID пользователя:', value=member.id, inline=False)
    emb.add_field(name='Points:', value=sql.execute('SELECT points FROM users WHERE id = {}'.format(member.id)).fetchone()[0], inline=False)
    emb.set_thumbnail(url=str(member.avatar_url))
    emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user:discord.Member,*,reason=None):
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f'{user.name}#{user.discriminator}  исключен', icon_url=user.avatar_url)
        await ctx.send(embed=emb)
        #logs
        channel = bot.get_channel(718960190703140955)
        await user.kick(reason=reason)
        emb = discord.Embed(title="`{}` исключен".format(user.name), colour=discord.Colour.red())
        emb.add_field(name="Причина:", value=reason)
        emb.add_field(name='ID пользователя:', value=user.id)
        emb.add_field(name='Модератор:', value="{}".format(ctx.author.name),inline=False)
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text=time_string)
        await channel.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user:discord.Member,*,reason=None):
        #logs
        await user.ban(reason=reason, delete_message_days=1)
        channel = bot.get_channel(718960190703140955)
        emb = discord.Embed(title="`{}` заблокирован".format(user.name), colour=discord.Colour.red())
        emb.add_field(name="Причина:", value=reason)
        emb.add_field(name='ID пользователя:', value=user.id)
        emb.add_field(name='Модератор', value="{}".format(ctx.author.name),inline=False)
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text='{}'.format(time_string))
        await channel.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def mut1e(ctx, user:discord.Member,*,time1=120):
        role = discord.utils.get(user.guild.roles, id=715186293549826068)
        channel = bot.get_channel(718960190703140955)
        await user.add_roles(role)
        emb = discord.Embed(title="{} заглушен".format(user.name), colour=discord.Colour.red())
        emb.add_field(name='ID пользователя:', value="{}".format(user.id))
        emb.add_field(name='Длительность:', value='{} минут'.format(int(time1)))
        emb.add_field(name='Модератор', value="{}".format(ctx.author.name),inline=False)
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text='{}'.format(time_string))
        await channel.send(embed=emb)

@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx,user:discord.Member):
    author = ctx.author
    role_names = [role.name for role in author.roles]
    if ("mute" in role_names):
            role = discord.utils.get(user.guild.roles, id=715186293549826068)
            emb = discord.Embed(title="`{}` заглушка снята ✅".format(user.name), colour=discord.Colour.orange())
            emb.set_footer(text='Администратором {}'.format(author.name), icon_url=author.avatar_url)
            await ctx.send(embed=emb)
            await user.remove_roles(role)
    else:
        sendd =f'{author.mention} _**Пользователь не заглушен!**_'
        await ctx.send(sendd)


@bot.command()
async def stats(ctx, member:discord.Member=None):
	await ctx.channel.purge(limit=1)
	if member is None:
		img = Image.new('RGBA', (400, 130), '#232529')
		url = str(ctx.author.avatar_url)[:-10]

		response = requests.get(url, stream = True)
		response = Image.open(io.BytesIO(response.content))
		response = response.convert('RGBA')
		response = response.resize((100, 100), Image.ANTIALIAS)

		img.paste(response, (15, 15, 115, 115))

		idraw = ImageDraw.Draw(img)
		name = ctx.author.name
		tag = ctx.author.discriminator

		headline = ImageFont.truetype('arial.ttf', size=20)
		undertext = ImageFont.truetype('arial.ttf', size=12)

		idraw.text((145,15), f'{name}#{tag}', font=headline )
		idraw.text((145,50), f'ID: {ctx.author.id}',font= undertext)
		idraw.text((145,70), f'Points: {sql.execute("""SELECT points FROM users WHERE id = {}""".format(ctx.author.id)).fetchone()[0]}',font= undertext)
		img.save('user_card.png')
		await ctx.send(file =discord.File(fp = "user_card.png"))
	else:
		img = Image.new('RGBA', (400, 130), '#232529')
		url = str(member.avatar_url)[:-10]

		response = requests.get(url, stream = True)
		response = Image.open(io.BytesIO(response.content))
		response = response.convert('RGBA')
		response = response.resize((100, 100), Image.ANTIALIAS)

		img.paste(response, (15, 15, 115, 115))

		idraw = ImageDraw.Draw(img)
		name = member.name
		tag = member.discriminator

		headline = ImageFont.truetype('arial.ttf', size=20)
		undertext = ImageFont.truetype('arial.ttf', size=12)

		idraw.text((145,15), f'{name}#{tag}', font=headline )
		idraw.text((145,50), f'ID: {member.id}',font= undertext)
		idraw.text((145,70), f'Points: {sql.execute("""SELECT points FROM users WHERE id = {}""".format(member.id)).fetchone()[0]}',font= undertext)
		img.save('user_card.png')
		await ctx.send(file =discord.File(fp = "user_card.png"))


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member:discord.Member, time = None, *, reason= None):
	role = discord.utils.get(member.guild.roles, id=715186293549826068)
	channel = bot.get_channel(718960190703140955)
	await member.add_roles(role)
	#answer
	emb = discord.Embed(colour=discord.Colour.red())
	emb.set_author(name=f'🔇 {member.name}#{member.discriminator} блокировка чата!',icon_url=member.avatar_url)
	await ctx.send(embed=emb)
	#log
	emb = discord.Embed(title="{} заглушен".format(member.name), colour=discord.Colour.red())
	emb.add_field(name='ID пользователя:', value="{}".format(member.id))
	emb.add_field(name='Длительность:', value='{} минут'.format(time))
	emb.add_field(name='Модератор:', value="{}".format(ctx.author.name))
	emb.add_field(name='Причина:',value=reason)
	emb.set_thumbnail(url=str(member.avatar_url))
	await channel.send(embed=emb)
	await asyncio.sleep(time)
	await member.remove_roles(role)
	emb = discord.Embed(title="{} заглушка снята".format(member.name), colour=discord.Colour.orange())
	emb.add_field(name='ID пользователя:', value="{}".format(member.id))
	emb.add_field(name='Модератор', value="Auto")
	emb.set_thumbnail(url=str(member.avatar_url))
	await channel.send(embed=emb)
       
token = os.environ.get("TOKEN")
bot.run(str(token))
