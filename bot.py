# Бот подписчик
import discord
from discord.ext import commands
import time
import os

prefix = "."
bot = commands.Bot(command_prefix=prefix)



#help
bot.remove_command('help')

@bot.command()
async def help(ctx):
    emb = discord.Embed(title="``Help``", colour=discord.Colour.orange())

    emb.add_field(name="{}vk".format(prefix), value="VK community.\nГруппа в ВК.")
    emb.add_field(name="{}leaders".format(prefix), value="Former leaders.\nБывшие лидеры.")

    await ctx.send(embed=emb)

# vk
@bot.command()
async def vk(ctx):
    author = ctx.author
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=discord.Embed(description=f'{author.mention} link to VK group: https://vk.com/gods_raga',colour=discord.Colour.dark_blue()))

#leaders

@bot.command()
async def leaders(ctx):
    emb = discord.Embed(title="Former leaders of the HCN clan!\nБывшие лидеры клана HCN!", colour=discord.Colour.orange())

    emb.add_field(name="2017-2019".format(prefix), value="HCN ⚡️Glitter")
    emb.add_field(name="2019-2020".format(prefix), value="HCN ⚡️Negative")

    await ctx.send(embed=emb)





@bot.event
async def on_ready():
    game=discord.Game("Hurricane [.help]")
    await bot.change_presence(status=discord.Status.online,activity=game)
    print("Бот запущен!")

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Ready.')
    print('------------')

    
            
token = os.environ.get("TOKEN")
bot.run(str(token))
