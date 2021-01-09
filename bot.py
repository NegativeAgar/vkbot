
import discord
from discord.ext import commands
import asyncio
import random
import os

import requests

bot = commands.Bot(command_prefix='!')


# Команда help
@bot.remove_command('help')

@bot.event
async def on_ready():
	game = discord.Game("Anarchy")
	await bot.change_presence(status=discord.Status.online, activity=game)
	print("Бот запущен!")
@bot.event
async def on_message(msg):
	rus = ["й","ц","у","к","е","н","г","ш","щ","з","х","ъ","ф","ы","в","а","п","р","о","л","д","ж","э","я","ч","с","м","и","т","ь","б","ї","і"]
	eng = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
	turk = ["ç","ğ","ı","ö","ş","ü"]
	channel_turk = bot.get_channel(787644954871595041)
	channel_russ = bot.get_channel(787713893882921000)
	channel_gen = bot.get_channel(797083742002216980)
	role = discord.utils.get(msg.author.guild.roles, id=787811953178968105)
	if msg.author.id == 796247213693075488 or msg.author.id == 234395307759108106 or msg.author.id==  159985870458322944:
		pass
	else:
		if msg.channel == channel_gen:
			for i in msg.content:
				if i in turk or i in rus:
					g = ('⛔ '+ str(msg.author.mention) +' here General chat! only English language!')
			await channel_gen.send(g)
		if msg.channel == channel_russ:
			for i in msg.content:
				if i in turk:
					g = ('⛔ '+ str(msg.author.mention) +' here Russian chat! only Russian language!')
			await channel_russ.send(g)
		if msg.channel == channel_turk:
			for i in msg.content:
				if i in rus:
					g = ('⛔ '+ str(msg.author.mention) +' here Turkish chat! only Turkish language!')	
			await channel_turk.send(g)	

	await bot.process_commands(msg)

token = os.environ.get("TOKEN")
bot.run(str(token))
