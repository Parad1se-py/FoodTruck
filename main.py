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

@bot.slash_command()
async def load(ctx, name):
    if ctx.author.id != int(owner_id):
        return
    bot.load_extension(f'cogs.{name}')
    await ctx.respond(f'Loaded {name}')
    
@bot.slash_command()
async def unloaded(ctx, name):
    if ctx.author.id != int(owner_id):
        return
    bot.unload_extension(f'cogs.{name}')
    await ctx.respond(f'Unloaded {name}')
    
@bot.slash_command()
async def reload(ctx, name):
	if ctx.author.id != int(owner_id):
		return
	bot.unload_extension(f'cogs.{name}')
	bot.load_extension(f'cogs.{name}')
	await ctx.respond(f'Reloaded {name}')

# Load cogs
"""for foldername in os.listdir('./cogs'):
    for filename in os.listdir(f'cogs/{foldername}'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{foldername}.{filename[:-3]}')"""
            
bot.load_extension('cogs.shop', recursive=True)
bot.load_extension('cogs.profile', recursive=True)

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(f"Discord Version: {discord.__version__}")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = "/help"))

# Run the bot
bot.run(token)