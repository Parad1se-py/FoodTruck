import discord
import json
import os

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	owner_id = data["owner_id"]

# Intents
intents = discord.Intents.all()
# The bot
bot = discord.Bot(intents = intents, owner_id = owner_id)

# Load cogs
if __name__ == '__main__':
	for folder in os.listdir("cogs"):
		for filename in os.listdir(f"cogs/{folder}"):
			if filename.endswith(".py"):
				bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Cooking Food!"))

bot.run(token)