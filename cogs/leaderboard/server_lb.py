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
from discord.commands import Option

from utils import *
from data import *


class ServerLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    lb = discord.SlashCommandGroup('leaderboard', description='See who ranks the highest!')
    
    @lb.command(
        name='global',
        description='View the global leaderboard',
        usage='/leaderboard global'
    )
    async def global_lb(self, ctx: discord.ApplicationContext):
        lb_data = collection.find().sort("cash", -1)
        
        emb = discord.Embed(
            title='Global cash leaderboard',
            description='Don\'t see your name up here? Play more to earn more cash!',
            color=discord.Colour.teal()
        )
        
        index = 0

        for i, x in enumerate(lb_data, 1):
            if index == 10:
                return await ctx.respond(embed=emb)
            if 'cash' in x:
                cash = str(x['cash'])
            else:
                continue
            if i == 1:
                user = await self.bot.get_or_fetch_user(x['_id'])
                emb.add_field(
                    name=f"**#{i}** 🥇 {user.name}",
                    value=f"`${cash}`",
                    inline=False
                )
            elif i == 2:
                user = await self.bot.get_or_fetch_user(x['_id'])
                emb.add_field(
                    name=f"**#{i}** 🥈 {user.name}",
                    value=f"`${cash}`",
                    inline=False
                )
            elif i == 3:
                user = await self.bot.get_or_fetch_user(x['_id'])
                emb.add_field(
                    name=f"**#{i}** 🥉 {user.name}",
                    value=f"`${cash}`",
                    inline=False
                )
            else:
                emb.add_field(
                    name=f"**#{i}** {await self.bot.fetch_user(x['_id'])}",
                    value=f"`${cash}`",
                    inline=False
                )
            index += 1

        return await ctx.respond(embed=emb)

def setup(bot:commands.Bot):
    bot.add_cog(ServerLeaderboard(bot))