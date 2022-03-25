# A program that takes in a .pdf link and sends each page of the pdf as images in a discord channel.

# discord
from dotenv import load_dotenv
import discord
from discord.ext import commands

# to image
import fitz
import os

# downloading
from pathlib import Path
import requests

# input checking
import re

# globals
CURRENT_PDF_FILE = "pdf/CURRENT_FILE.pdf"
CURRENT_IMG_DIR = "image/CURRENT_FILE"

# discord====================================

load_dotenv()

bot = commands.AutoShardedBot(commands.when_mentioned_or('!'))
bot.remove_command("help")

@bot.event
async def on_ready():
    print('PDFtoJPEG bot ready')
    await bot.change_presence(activity=discord.Game(name="!info for help"))

@bot.command(aliases=['info'])
async def help(ctx):
    await ctx.send("To convert a pdf to images, use '!pdf [pdf link] [start] [end]'. \n\n" +
    	"Examples: \n" +
    	'"!pdf website.com/file.pdf" (sends all pages) \n' +
    	'"!pdf website.com/file.pdf 1 3" (sends pages 1 to 3) \n' +
    	'"!pdf website.com/file.pdf 5" (sends pages 5 to the end) \n\n' +
    	'Use "!pdf_me" to send to yourself.')

@bot.command()
async def pdf(ctx, pdf_link: str, start: float=1.0, end: float=-1.0):
	start = int(start)
	end = int(end)

	if valid(pdf_link, start, end):
		get_pdf(pdf_link)
		pdf_to_image(CURRENT_PDF_FILE)

		lst = os.listdir(CURRENT_IMG_DIR)
		if end == -1:
			end = len(lst)
	    
		#send images
		for i in range(start - 1, end):
			await ctx.channel.send(file=discord.File(f'{CURRENT_IMG_DIR}/{i}.jpg'))

		#remove image files after sending
		remove_images()
	else:
		await ctx.channel.send("Check your inputs")

@bot.command()
async def pdf_me(ctx, pdf_link: str, start: float=1.0, end: float=-1.0):
	start = int(start)
	end = int(end)

	if valid(pdf_link, start, end):
		get_pdf(pdf_link)
		pdf_to_image(CURRENT_PDF_FILE)

		lst = os.listdir(CURRENT_IMG_DIR)
		if end == -1:
			end = len(lst)
	    
		#send images
		for i in range(start - 1, end):
			await ctx.author.send(file=discord.File(f'{CURRENT_IMG_DIR}/{i}.jpg'))
		await ctx.channel.send("Done.")

		#remove image files after sending
		remove_images()
	else:
		await ctx.channel.send("Check your inputs")

# helpers===================================

def get_pdf(url: str) -> None:
	filename = Path(CURRENT_PDF_FILE)
	response = requests.get(url)
	filename.write_bytes(response.content)

def pdf_to_image(pdf_file: str) -> int:
	pdf_file = fitz.open(pdf_file)

	for idx, page in enumerate(pdf_file):
		pix = page.get_pixmap(matrix = fitz.Matrix(2, 2)) # 2 is zoom factor for resolution
		pix.save(f"{CURRENT_IMG_DIR}/{idx}.jpg")

def valid(pdf_link: str, start: int, end: int) -> bool:
	return ((end >= start or (start == 1 and end == -1) or end == -1) and 
		start >= 1 and 
		end >= -1 and 
		end != 0 and 
		re.match("^.*\\.pdf$", pdf_link) and 
		re.match("^\\d*$", str(start)) and 
		re.match("^\\d*$", str(end)))

def remove_images() -> None:
	for path in os.listdir(CURRENT_IMG_DIR):
		full_path = os.path.join(CURRENT_IMG_DIR, path)
		if os.path.isfile(full_path):
			os.remove(full_path)

bot.run('YOUR_DISCORD_TOKEN')
