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
from discord.commands import Option
from discord.ext import commands, pages, tasks

from data import *
from utils import *


@tasks.loop(seconds = 3600)
async def stock_updater():
    """Looper to set price for the stocks, based on how much people buy it."""
    print("UPDATING STOCKS DATA")

    for i, j in stocks.items():
        if j['bought'] >= 4:
            x = random.randint(100, 250)
            new_price = x * j['bought']
            update_stockup_count(i, -1 * j['bought'])
            set_stockup_count(i, 0)
            update_stock_price(i, new_price)
            update_stock_type(i, '🔼')
            update_stock_count(i, random.randint(1, 5))
        elif j['bought'] < 3:
            new_price = 50 * j['bought']
            update_stockup_count(i, -1 * j['bought'])
            set_stockup_count(i, 0)
            update_stock_price(i, -1 * new_price)
            update_stock_type(i, '🔽')
            update_stock_count(i, random.randint(1, 3))


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profit = '🔼'
        self.loss = '🔽'
        self.loaded_stocks_list = [x for x, y in stocks.items()]
        self.pages = get_market_embed_pages()

    def get_pages(self):
        return self.pages

    async def stocks_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_stocks_list if item.startswith(ctx.value.lower()) or item.lower() == ctx.value.lower()]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        stock_updater.start()

    stocks_slash_group = discord.SlashCommandGroup(name='stocks', description='All commands related to FoodTruck Stocks!')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @stocks_slash_group.command(
        name='buy',
        description='Buy stocks (if available) from the market (/stocks market)!',
        usage='/stocks buy [stock_id] <amount>'
    )
    async def buy_stocks(self, 
                         ctx: discord.ApplicationContext,
                         item: Option(str, required=True, autocomplete=stocks_searcher),
                         amount: Option(int, required=False)):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")
        await ctx.defer()

        udata = get_user_data(ctx.author)
        if udata['cash'] < int(amount) * get_stock_data(item)['price']:
            return await ctx.respond("You don't have enough money to buy those many shares.")

        for i, j in stocks.items():
            if i == item:
                if j['amt'] < int(amount):
                    return await ctx.respond(f"There aren't that many shares available.\nOnly `{j['amt']}` shares are available for {i}.")

                if j['amt'] == 0:
                    return await ctx.respond(f"There aren't any shares for {i} available, check back later.")

                update_l(ctx.author.id, 5)
                update_data(ctx.author, 'cash', -1* (int(amount) * get_stock_data(item)['price']))
                add_stock(ctx.author, str(item.lower()), int(amount))
                update_stock_count(item, -1 * int(amount))
                update_stockup_count(item, int(amount))
                return await ctx.respond(f"You have bought `{amount}` shares of `{item}`.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @stocks_slash_group.command(
        name='sell',
        description='Sell stocks (if owned) to the market (/stocks market)!',
        usage='/stocks sell [stock_id] <amount>'
    )
    async def sell_stocks(self, 
                         ctx: discord.ApplicationContext,
                         item: Option(str, required=True, autocomplete=stocks_searcher),
                         amount: Option(int, required=False)):
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        if amount <= 0:
            return await ctx.reply(f"You can't sell less than 1 share, {ctx.author.name}!")

        await ctx.defer()

        if not check_for_stock(ctx.author, item):
            return await ctx.reply(f"You don't have any shares of that stock, {ctx.author.name}!")

        if stock_count(ctx.author, item) < amount:
            return await ctx.reply(f"You don't have that many shares, {ctx.author.name}!")

        for i, j in stocks.item():
            if i == item:
                update_l(ctx.author.id, 10)
                add_stock(ctx.author, item, -amount)
                update_stock_count(item, amount)
                update_data(ctx.author, 'wallet', amount * get_stock_data(item)['price'])
                return await ctx.reply(f"You have sold `{amount}` shares of `{item}`.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @stocks_slash_group.command(
        name='market',
        description='Shows the FoodTruck stock market!',
        usage='/stocks market'
    )
    async def market(self, ctx:discord.ApplicationContext):
        await ctx.defer()

        paginator = pages.Paginator(
            pages = self.get_pages(),
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=True,
            loop_pages=True,
            disable_on_timeout=True,
            timeout=15
        )
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot:commands.Bot):
    bot.add_cog(Stocks(bot))
