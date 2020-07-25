# Бот подписчик
import discord
from discord.ext import commands
import asyncio
import random
import time
import os


time_string = time.strftime("%A %X")

prefix = "."
bot = commands.Bot(command_prefix=prefix)


# Команда help
bot.remove_command('help')


# clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count=20):
    author = ctx.message.author
    await ctx.channel.purge(limit=count)
    await ctx.send(embed=discord.Embed(description=f'Чат очистил администратор: {author.mention}'))
    time.sleep(3.0)
    await ctx.channel.purge(limit=1)

# Чат бот
@bot.command()
async def sostav(ctx):
        author = ctx.author
        await ctx.send(f" {author.mention}, если ты это написал, значит ты не в составе :)")

@bot.command()
async def point(ctx):
		author = ctx.author

		emb = discord.Embed(title="Рейтинг Point's", colour=discord.Colour.orange())
		emb.add_field(name="Участники:",value="JayBy [`7`] points\nCastia [`7`] points\nFlycks [`0`] points")
		await ctx.send(embed=emb)



# Подключение к каналу
@bot.event
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.guild.roles, id=712600261012488242)
    await member.add_roles(role)



# commands
@bot.command()
async def help(ctx):
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title="Помощь по боту", colour=discord.Colour.orange())
        emb.add_field(name='Команды:',value='`.info @id` - Посмотреть статистику'
                            '\n`.sostav` - Состав команды!',inline=False)
        await ctx.send(embed=emb)



# info
@bot.command()
async def info(ctx, user: discord.Member):
    emb = discord.Embed(title="Статистика `{}`".format(user.name), colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.add_field(name='Имя:', value=user.name)
    emb.add_field(name="Зашёл на канал:", value=str(user.joined_at)[:10])
    emb.add_field(name='ID пользователя:', value=user.id, inline=False)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user:discord.Member,*,reason=None):
        channel = bot.get_channel(718960190703140955)
        await user.kick(reason=reason)
        emb = discord.Embed(title="`{}` исключен".format(user.name), colour=discord.Colour.red())
        emb.add_field(name="Причина:", value=reason)
        emb.add_field(name='ID пользователя:', value=user.id)
        emb.add_field(name='Модератор', value="{}".format(ctx.author.name),inline=False)
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text=time_string)
        await channel.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user:discord.Member,*,reason=None):
        await user.ban(reason=reason, delete_message_days=1)
        channel = bot.get_channel(718960190703140955)
        emb = discord.Embed(title="`{}` забанен".format(user.name), colour=discord.Colour.red())
        emb.add_field(name="Причина:", value=reason)
        emb.add_field(name='ID пользователя:', value=user.id)
        emb.add_field(name='Модератор', value="{}".format(ctx.author.name),inline=False)
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text='{}'.format(time_string))
        await channel.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, user:discord.Member,*,time1=120):
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
        time.sleep(time1*60)
        emb = discord.Embed(title="{} заглушка снята".format(user.name), colour=discord.Colour.orange())
        emb.add_field(name='ID пользователя:', value="{}".format(user.id))
        emb.add_field(name='Модератор', value="Auto")
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text=time_string)
        await channel.send(embed=emb)
        await user.remove_roles(role)

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

@bot.event
@commands.has_permissions(administrator=True)
async def on_message(msg):
    reacit = [".ban", ".mute", ".kick", ".unmute"]
    author = msg.author
    channel = msg.channel
    for i in reacit:
        if i in msg.content:
           await msg.add_reaction('✅')
    await bot.process_commands(msg)


@bot.event
async def on_ready():
    game = discord.Game("Помощь [.help] ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Бот запущен!")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Ready.')
    print('------------')
            




            
token = os.environ.get("TOKEN")
bot.run(str(token))
