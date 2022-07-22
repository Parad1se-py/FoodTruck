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

import discord
from discord.ext import commands
from discord.commands import Option

from utils import *
from data import *


class Cook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='cook',
        description='Cook any item that you have unlovked from the menu!',
        usage='/cook'
    )
    async def cook(self,
                   ctx: discord.ApplicationContext,
                   dish: Option(str, required=True),
                   amount: Option(int, required=False)=1):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        user_data = get_user_data(ctx.author.id)

        for key, value in menu.items():
            if key.lower() == dish.lower() or value[0].lower() == dish.lower():
                if user_data['level'] < value[4]:
                    return await ctx.respond(f"You don't have the required level (`{value[4]}`) to cook this dish! Your current level is `{user_data['level_l']/10}`")

                for ingredient in user_data['inv']:
                    if not check_for_item(ctx.author.id, ingredient):
                        return await ctx.respond(f"You lack the ingredient `{ingredient}`! Buy it using `/buy {ingredient}`.")
                    count = item_count(ctx.author.id, ingredient)
                    if count < amount:
                        return await ctx.respond(f"You lack {amount}x `{ingredient}`! You currently have `{count}` {ingredient}. Buy the required amount using `/buy {ingredient} {amount-count}`.")

                for ingredient in user_data['inv']:
                    remove_item(ctx.author.id, ingredient, amount)

                add_active(ctx.author, dish, amount)
                msg = await ctx.respond(f"Your dish is being prepared! Come back in {value[5]/60:.1f} minute(s).")
                asyncio.sleep(value[5])
                remove_active(ctx.author.id)
                add_dish(ctx.author, dish, amount)
                await ctx.edit(f"`{amount}`x **{key}** has been prepared!")
            else:
                return await ctx.respond("No such dish... Look up some dishes via `/menu`!")


def setup(bot:commands.Bot):
    bot.add_cog(Cook(bot))