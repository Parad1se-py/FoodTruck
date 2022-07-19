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
from discord.ext import commands
from discord.commands import Option

from utils import *
from data import *


class Ingredients_Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='shop',
        description='View the ingredients shop!',
        usage='/shop'
    )
    async def shop(self, ctx):
        shop_embed = discord.Embed(
            title="FoodTruck Ingredients Shop!",
            descripton="Use `/buy [item_id] <amt>` to buy any ingredient!",
            color=discord.Colour.teal()
        )

        for key, value in ing_shop:
            shop_embed.add_field(
                name=f"{value[2]} {key}",
                value=f"`${value[1]}` | Id : `{value[0]}`",
                inline=False
            )

        return await ctx.respond(embed=shop_embed)
    
    @commands.slash_command(
        name='buy',
        description='Buy an ingredient from the shop `/shop`',
        usage='/buy [item] <amount>'
    )
    async def buy(self,
                  ctx,
                  item: Option(str, required=True),
                  amount: Option(int, requried=False)=1):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

def setup(bot:commands.Bot):
    bot.add_cog(Ingredients_Shop(bot))