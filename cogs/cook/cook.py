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
import datetime
import random

import discord
from discord.ext import commands
from discord.commands import Option

from utils import *
from data import *


class Cook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_menu_list = [x for x, y in menu.items()]

    async def item_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_menu_list if item.lower().startswith(ctx.value.lower()) or item.lower() == ctx.value.lower()]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='cook',
        description='Cook any item that you have unlovked from the menu!',
        usage='/cook'
    )
    async def cook(self,
                   ctx: discord.ApplicationContext,
                   dish: Option(str, required=True, autocomplete=item_searcher),
                   amount: Option(int, required=False)=1):
        await ctx.defer()
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        user_data = get_user_data(ctx.author.id)

        for key, value in menu.items():
            if key == dish:
                if user_data['level'] < value[4]:
                    return await ctx.respond(f"You don't have the required level (`{value[4]}`) to cook this dish! Your current level is `{user_data['level']}`")

                for ingredient in value[1]:
                    if not check_for_item(ctx.author.id, ingredient):
                        return await ctx.respond(f"You lack the ingredient `{ingredient}`! Buy it using `/buy {ingredient}`.")
                    count = item_count(ctx.author.id, ingredient)
                    if count < amount:
                        return await ctx.respond(f"You lack {amount}x `{ingredient}`! You currently have `{count}` {ingredient}. Buy the required amount using `/buy {ingredient} {amount-count}`.")
                    remove_item(ctx.author.id, ingredient, amount)

                if bool(user_data['dishes_cooked']) == False:
                    add_badge(ctx.author.id, 'first-dish-badge')

                add_active(ctx.author, dish, amount*value[2])
                msg = await ctx.respond(f"Your dish is being prepared! Come back {convert_to_unix_time(datetime.datetime.now(), seconds=value[5])}.")
                await asyncio.sleep(value[5])
                remove_active(ctx.author.id, dish, amount*value[2])
                add_dish(ctx.author, dish, amount*value[2])
                inc_dishes_cooked(ctx.author.id, dish, amount*value[2])
                await update_l(ctx.author.id, amount*(random.randint(1, 3)))

                await msg.edit(f"`{amount*value[2]}`x **{key}** has been prepared!")

                try:
                    return await ctx.author.send(f"`{amount*value[2]}`x **{key}** has been prepared!")
                except Exception as e:
                    raise e

        return await ctx.respond("No such dish... Look up some dishes via `/menu`!")

def setup(bot:commands.Bot):
    bot.add_cog(Cook(bot))
