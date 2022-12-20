# A program that takes in a .pdf link and sends each page of the pdf as images in a discord channel.

import discord
from discord.ext import commands
import asyncio
import config
import os

# globals
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all(), application_id="893744535191031840")
bot.remove_command("help")

@bot.event
async def on_ready():
	print('PDFtoJPEG bot ready')
	await bot.change_presence(activity=discord.Game(name="!info for help"))

@bot.command()
async def info(ctx):
	await ctx.send("To use, do: /pdf")

@bot.event
async def on_message(message):
	await bot.process_commands(message)

async def load():
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
	await load()
	await bot.start(config.get_token())

asyncio.run(main())

