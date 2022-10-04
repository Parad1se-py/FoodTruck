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


class Bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='bet',
        descrpition='Bet your money to get a return from 25-100%',
        usage='/bet [bet]'
    )
    async def bet(self,
                  ctx: discord.ApplicationContext,
                  bet: Option(int, 'Money to gamble', required=True)):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        if bet < 200:
            return await ctx.respond("You need to bet atleast `$200`!")

        cash = get_user_data(ctx.author.id)['cash']

        if cash < bet:
            return await ctx.respond(f"You don't have `${bet}`! You only have `${cash}`.")

        embed = discord.Embed(
            title='Betting...',
            color=discord.Colour.teal()
        )
        msg = await ctx.respond(embed=embed)
        await asyncio.sleep(1.5)

        player_strikes, bot_strikes = random.randint(1, 12), random.randint(3, 12)

        if player_strikes > bot_strikes:
            percent = random.randint(25, 100)
            amount_won = int(bet*(percent/100))
            update_data(ctx.author.id, 'cash', amount_won)

            emb = discord.Embed(
                title=f'{ctx.author.name}\'s Bet Results',
                description=f'You won `${amount_won}`!\nPercent won: **{percent}%**',
                color=discord.Colour.teal()
            )

        elif bot_strikes > player_strikes:
            update_data(ctx.author.id, 'cash', -bet)

            emb = discord.Embed(
                title=f'{ctx.author.name}\'s Bet Results',
                description=f'You lost `${bet}`...',
                color=discord.Colour.teal()
            )

        elif bot_strikes == player_strikes:
            emb = discord.Embed(title=f'{ctx.author.name}\'s Bet Results', description='No one won! It was a tie.', color=discord.Colour.teal())


        emb.add_field(
            name='Player Strikes:',
            value=f'`{player_strikes}`'
        )
        emb.add_field(
            name='FoodTruck Strikes:',
            value=f'`{bot_strikes}`'
        )

        return await msg.edit_original_message(embed=emb)

def setup(bot:commands.Bot):
    bot.add_cog(Bet(bot))
