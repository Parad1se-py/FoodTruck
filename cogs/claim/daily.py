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

import random

import discord
from discord.ext import commands
from discord.commands import Option

from utils import *


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")

    @commands.slash_command(
        name='daily',
        description='Reedem your daily cash and free ingredients!',
        usage='/daily'
    )
    @commands.cooldown(86400, 1, commands.BucketType.user)
    async def daily(self, ctx: discord.ApplicationContext):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")
        
        cash = random.randint(50, 550)

        update_data(ctx.author.id, 'cash', cash)
        
        embed = discord.Embed(
            title='Daily loot reedemed!',
            description=f'You reedemed `${cash}`!',
            color=discord.Colour.teal()
        )
        
        return await ctx.respond(embed=embed)
        
def setup(bot:commands.Bot):
    bot.add_cog(Daily(bot))