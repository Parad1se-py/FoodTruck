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


class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='slots',
        description='Bet some cash on the slots machine, it\'s a win-or-lose situation!',
        usage='/slots [bet]'
    )
    async def slots(self,
                    ctx: discord.ApplicationContext,
                    bet: Option(int, 'Money to gamble', required=True)):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")
        
        if bet < 200:
            return await ctx.respond("You need to bet atleast `$200`!")

        cash = get_user_data(ctx.author.id)['cash']

        if cash < bet:
            return await ctx.respond(f"You don't have `${bet}`! You only have `${cash}`.")

        embed = discord.Embed(
            title='Rolling the slots machine',
            color=discord.Colour.teal()
        )
        msg = await ctx.respond(embed=embed)
        await asyncio.sleep(2)

        slots = [random.choice(['🌮', '🌭', '🥞']), random.choice(['🌮', '🌭', '🥞']), random.choice(['🌮', '🌭', '🥞'])]

        if slots[0] == slots[1] == slots[2]:
            emb = discord.Embed(
                title=f'{ctx.author.name}\'s Slot Machine Roll',
                description=f'`{slots[0]} | {slots[1]} | {slots[2]}`\nCash won: `${bet*2}`',
                color=discord.Colour.teal()
            )
            update_data(ctx.author.id, 'cash', bet*2)
        elif slots[0] == slots[1] or slots [1] == slots[2] or slots[2] == slots[0]:
            emb = discord.Embed(
                title=f'{ctx.author.name}\'s Slot Machine Roll',
                description=f'`{slots[0]} | {slots[1]} | {slots[2]}`\nCash won: `${bet+(bet*0.5)}`',
                color=discord.Colour.teal()
            )
            update_data(ctx.author.id, 'cash', bet+(bet*0.5))
        else:
            emb = discord.Embed(
                title=f'{ctx.author.name}\'s Slot Machine Roll',
                description=f'`{slots[0]} | {slots[1]} | {slots[2]}`\nCash lost: `${bet}`',
                color=discord.Colour.teal()
            )
            update_data(ctx.author.id, 'cash', -bet)

        await msg.edit(embed=emb)

def setup(bot:commands.Bot):
    bot.add_cog(Slots(bot))