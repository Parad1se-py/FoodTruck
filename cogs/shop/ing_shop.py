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

import json

import discord
from discord import guild_only, slash_command
from discord.ext import commands
from discord.commands import slash_command, Option

from utils import *

with open('./ing_shop.json', 'r') as f:
    shop = json.load(f)


class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @guild_only()
    @slash_command(
        name='shop',
        usage='/shop',
        description='View the ingredients shop!'
    )
    async def shop(self, ctx):
        shop_embed = discord.Embed(
            title="FoodTruck Ingredients Shop!",
            descripton="Use `/buy [item_id] <amt>` to buy any ingredient!",
            color=discord.Colour.teal()
        )
        
        for item in shop:
            shop_embed.add_field(
                name=f"{item['pic']} {item}",
                value=f"${item['price']}"
            )
            
        return await ctx.respond(embed=shop_embed)