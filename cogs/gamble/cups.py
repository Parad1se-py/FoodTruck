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

import asyncio
import random

import discord
from discord.ext import commands
from discord.commands import Option

from utils import *


class Cups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='cups',
        description='Gamble your money to guess the cup which has candy under it!',
        value='/cups [bet]'
    )
    async def cups(self,
                   ctx: discord.ApplicationContext,
                   bet: Option(int, required=True)):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")
        
        if bet < 200:
            return await ctx.respond("You need to bet atleast `$200`!")

        cash = get_user_data(ctx.author.id)['cash']

        if cash < bet:
            return await ctx.respond(f"You don't have `${bet}`! You only have `${cash}`.")

        embed = discord.Embed(
            title='Here\'s the candy!',
            description="""
            
            """,
            color=discord.Colour.teal()
        )
        msg = await ctx.respond(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Cups(bot))