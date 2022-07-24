# -*- coding: utf-8 -*-
# Copyright (c) 2022 Parad1se-py

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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


@bot.slash_command(guild_ids=[765869842451398667])
async def load(ctx, name):
    if ctx.author.id != int(owner_id):
        return
    bot.load_extension(f'cogs.{name}')
    await ctx.respond(f'Loaded {name}')
    
@bot.slash_command(guild_ids=[765869842451398667])
async def unloaded(ctx, name):
    if ctx.author.id != int(owner_id):
        return
    bot.unload_extension(f'cogs.{name}')
    await ctx.respond(f'Unloaded {name}')
    
@bot.slash_command(guild_ids=[765869842451398667])
async def reload(ctx, name):
	if ctx.author.id != int(owner_id):
		return
	bot.unload_extension(f'cogs.{name}')
	bot.load_extension(f'cogs.{name}')
	await ctx.respond(f'Reloaded {name}')


# Load cogs
for foldername in os.listdir('cogs'):
    for filename in os.listdir(f'cogs/{foldername}'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{foldername}.{filename[:-3]}', store=False)


@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(f"Discord Version: {discord.__version__}")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = "Preparing dishes!"))

# Run the bot
bot.run(token)