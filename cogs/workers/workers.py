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


class Workers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_worker_list = [x for x, y in workers.items()]

    async def stocks_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_worker_list if item.startswith(ctx.value.lower()) or item.lower() == ctx.value.lower()]
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")

    workers_slash_group = discord.SlashCommandGroup(name='worker', description='All commands related to FoodTruck Worker Bots!')

    @workers_slash_group.command(
        name='buy',
        description='Buy a new worker bot',
        usage='/worker buy [id/name] <amount>'
    )
    async def worker_buy(self,
                         ctx: discord.ApplicationContext,
                         name: Option(str, required=True, autocomplete=stocks_searcher),
                         amount: Option(int, required=False)=1):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        udata = get_user_data(ctx.author.id)

        for x, y in workers.items():
            if x == name:
                if udata['cash'] < int(amount) * y[1]:
                    return await ctx.respond("You don't have enough money to buy those many workers.")

                if amount < 3:
                    await update_l(ctx.author.id, amount*3)
                else:
                    await update_l(ctx.author.id, amount*2)

                add_workers(ctx.author.id, name, amount)
                update_data(ctx.author.id, 'cash', -amount*y[1])

                success_embed = discord.Embed(
                    title="Successful Purchase",
                    description=f'You successfully bought `{amount}`x {x} worker for `${amount*y[1]}`!',
                    color=discord.Colour.teal()
                )
                success_embed.set_footer(text='Thanks for your purchase! Happy cooking :)')

                return await ctx.respond(embed=success_embed)

    @workers_slash_group.command(
        name='sell',
        description='Sell an owned worker bot',
        usage='/worker sell [id/name] <amount>'
    )
    async def worker_buy(self,
                         ctx: discord.ApplicationContext,
                         name: Option(str, required=True, autocomplete=stocks_searcher),
                         amount: Option(int, required=False)=1):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        for x, y in workers.items():
            if x == name:
                if workers_count < amount:
                    return await ctx.respond(f"You don't have those many {x} workers!")

                if amount < 3:
                    await update_l(ctx.author.id, amount*3)
                else:
                    await update_l(ctx.author.id, amount*2)

                remove_workers(ctx.author.id, name, amount)
                update_data(ctx.author.id, 'cash', amount*(y[1]/10))

                success_embed = discord.Embed(
                    title="Successful Sale",
                    description=f'You successfully sold `{amount}`x {x} worker for `${amount*(y[1]/10)}`!',
                    color=discord.Colour.teal()
                )
                success_embed.set_footer(text='https://discord.gg/VVfvtFV3qu')

                return await ctx.respond(embed=success_embed)


def setup(bot:commands.Bot):
    bot.add_cog(Workers(bot))
