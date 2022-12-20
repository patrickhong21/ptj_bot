#discord
import discord
from discord.ext import commands
from discord import app_commands

# to image
import fitz
import os

# downloading
import pathlib
import requests

# input checking
import re

CURRENT_PDF_FILE = f"{os.getcwd()}/pdf/CURRENT_FILE.pdf"
CURRENT_IMG_DIR = f"{os.getcwd()}/image/CURRENT_FILE"
MAX_PAGES = 20

class PDFCommands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("PDFCommands Cog loaded")

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def sync(self, ctx: commands.Context):
		fmt = await ctx.bot.tree.sync()
		await ctx.send(f"Synced {len(fmt)} commands.")

	@app_commands.command(name="pdf", description="Converts a PDF link into images")
	@app_commands.describe(pdf_link="the link ending in .pdf")
	@app_commands.describe(start="starting page (default is 1)")
	@app_commands.describe(end="ending page (default is last page up to 20)")
	@app_commands.describe(send_to_all="0 to disallow and 1 to allow others to see the images")
	async def pdf(
		self,
		interaction: discord.Interaction,
		pdf_link: str,
		start: app_commands.Range[int, 1, MAX_PAGES - 1] = 1,
		end: app_commands.Range[int, 2, MAX_PAGES] = -1,
		send_to_all: app_commands.Range[int, 0, 1] = 0):

		if self.valid(pdf_link, start, end):
			self.get_pdf(pdf_link)
			self.pdf_to_image(CURRENT_PDF_FILE)

			lst = os.listdir(CURRENT_IMG_DIR)
			if end == -1:
				end = len(lst)
			if end > MAX_PAGES:
				end = MAX_PAGES

			#send images
			for i in range(start - 1, end):
				file = discord.File(f'{CURRENT_IMG_DIR}/{i}.jpg')
				if i == start - 1:
					await interaction.response.send_message(file=file, ephemeral=(not bool(send_to_all)))
				# work around to send multiple messages
				else: 
					await interaction.followup.send(file=file, ephemeral=(not bool(send_to_all)))

			#remove image files after sending
			self.remove_images()
		else:
			await interaction.response.send_message("Check your inputs", ephemeral=True)

	# helpers

	def get_pdf(self, url: str) -> None:
		filename = pathlib.Path(CURRENT_PDF_FILE)
		response = requests.get(url)
		filename.write_bytes(response.content)

	def pdf_to_image(self, pdf_file: str) -> None:
		pdf_file = fitz.open(pdf_file)

		for idx, page in enumerate(pdf_file):
			pix = page.get_pixmap(matrix = fitz.Matrix(2, 2)) # 2 is zoom factor for resolution
			pix.save(f"{CURRENT_IMG_DIR}/{idx}.jpg")

	def valid(self, pdf_link: str, start: int, end: int) -> bool:
		return ((end >= start or (start == 1 and end == -1) or end == -1) and 
			start >= 1 and 
			end >= -1 and 
			re.match("^.*\\.pdf$", pdf_link))

	def remove_images(self) -> None:
		for path in os.listdir(CURRENT_IMG_DIR):
			full_path = os.path.join(CURRENT_IMG_DIR, path)
			if os.path.isfile(full_path):
				os.remove(full_path)

async def setup(bot):
	await bot.add_cog(PDFCommands(bot))
