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
from data import *


class Serve(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_menu_list = [x for x, y in menu.items()]

    async def item_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_menu_list if item.startswith(ctx.value.lower())]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.slash_command(
        name='serve',
        description='Serve cooked food to your customers!',
        usage='/serve [item] <amount>'
    )
    async def serve(
        self,
        ctx: discord.ApplicationContext,
        dish: Option(str, description='ID/Name of the dish being served', required=True, autocomplete=item_searcher),
        amount: Option(str, description='Amount of the dish that you want to serve', required=False)=1
    ):
        if not check_acc(ctx.author.id):
            return await ctx.respond("You don't have an account as you haven't played yet! Start with `/daily`!")

        await ctx.defer()

        for key, val in menu.items():
            if dish.lower() not in [key, val[0]]:
                continue
            if not check_for_dish(ctx.author.id, val[0]):
                return await ctx.respond(
                    "You don't have that dish ready."
                )

            dish_amt = int(dish_count(ctx.author.id, val[0]))
            if dish_amt == 0:
                return await ctx.respond(
                    "You don't have that dish ready; cook it."
                )
            amount = dish_amt if amount in ['all', 'max'] else int(amount)

            if dish_amt < amount:
                return await ctx.respond(
                    f"You don't have `{amount}` {key}! You only have `{dish_amt}` {key}."
            )

            await update_l(ctx.author.id, int(amount*(random.randint(1, 3))))
            remove_dish(ctx.author.id, val[0], amount)
            update_data(ctx.author.id, 'cash', amount*val[6])

            success_embed = discord.Embed(
                title=f"{key} served!",
                description=f"You served `{amount*val[2]}x` {key} for `${amount*val[6]}`!",
                color=discord.Colour.teal()
            )

            return await ctx.respond(embed=success_embed)

        return await ctx.respond(
            f"The dish {dish} was not found!"
        )

def setup(bot:commands.Bot):
    bot.add_cog(Serve(bot))
