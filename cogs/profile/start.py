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
from discord.ext import commands

from utils import *


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='start',
        description='Get started with FoodTruck, create an account and get some freebies!',
        usage='/start'
    )
    async def start(self, ctx:discord.ApplicationContext):
        if not check_acc(ctx.author.id):
            register(ctx.author)
            embed = discord.Embed(
                title='Registered successfully!',
                description='I have added `$500` cash to start with, and `cheese`, `veg-fillings` & `taco-shell` to your kitchen as well!',
                color=discord.Colour.teal()
            )
            embed.add_field(
                name='Cook your first item!:',
                value='1. Buy cheese `/buy cheese`\n2.Cook a taco! `/cook taco`',
                inline=False
            )
            embed.add_field(
                name='> **🤔 Don\'t know what to do?**',
                value='Use `/help` to view more commands!',
                inline=False
            )

            return await ctx.respond(embed=embed)
        return await ctx.respond('You already seem to have an account! View your profile using `/profile`')
        
def setup(bot:commands.Bot):
    bot.add_cog(Start(bot))