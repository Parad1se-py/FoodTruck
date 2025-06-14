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
from discord.ext import commands, tasks
from discord.commands import Option

from utils import *


class Workers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_worker_list = [x for x, y in workers.items()]
        self.loaded_menu_list = [x for x, y in menu.items()]

    async def worker_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_worker_list if item.startswith(ctx.value.lower()) or item.lower() == ctx.value.lower()]
    
    async def dish_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_menu_list if item.lower().startswith(ctx.value.lower()) or item.lower() == ctx.value.lower()]


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
                         name: Option(str, required=True, autocomplete=worker_searcher),
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
                success_embed.set_footer(text='Thanks for your purchase! Happy cooking :) | https://discord.gg/VVfvtFV3qu')

                return await ctx.respond(embed=success_embed)

    @workers_slash_group.command(
        name='sell',
        description='Sell an owned worker bot',
        usage='/worker sell [id/name] <amount>'
    )
    async def worker_sell(self,
                         ctx: discord.ApplicationContext,
                         name: Option(str, required=True, autocomplete=worker_searcher),
                         amount: Option(int, required=False)=1):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        for x, y in workers.items():
            if x == name:
                if workers_count(ctx.author.id, x) < amount:
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


    @workers_slash_group.command(
        name='start',
        description='Start your worker machines to automatically cook food!',
        usage='/worker start [recipe] <amount=1>'
    )
    async def worker_start(self,
                           ctx: discord.ApplicationContext,
                           worker_bot: Option(str, required=True, autocomplete=worker_searcher),
                           recipe: Option(str, required=True, autocomplete=dish_searcher),
                           amount: Option(int, required=False)=10
                           ):
        # TODO: Check if amount is within worker limit and ask for the worker they wanna use :sob:
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")
        
        if amount < 10:
            return await ctx.respond("You cannot enter an amount lesser than 11!\nTo cook a recipe for an amount less than 11, use `/cook`.")

        if recipe not in menu:
            return await ctx.respond(f"The recipe `{recipe}` does not exist.\nCheck existing recipes using `/menu`!")
        
        user_id = ctx.author.id
        user_inventory = get_user_data(user_id)['inv']

        required_ingredients = menu[recipe][1]
        cooking_time = menu[recipe][5]
        quantity = menu[recipe][2]*amount

        # check if user has all required ingredients
        for ingredient in required_ingredients:
            if not check_for_item(ctx.author.id, ingredient):
                return await ctx.respond(f"You lack the ingredient `{ingredient}`! Buy it using `/buy {ingredient}`.")
            count = user_inventory[ingredient]
            if count < amount:
                return await ctx.respond(f"You lack {amount}x `{ingredient}`! You currently have `{count}` {ingredient}. Buy the required amount using `/buy {ingredient} {amount-count}`.")
            
        # check if amount of food being cooked is above limit of the worker bot
        if quantity > workers[worker_bot][3]:
            return await ctx.respond(f"You cannot cook {amount}x `{recipe}` since it exceeds the limit of your worker bot ({workers[worker_bot][3]}x)\nEnter a lower amount, or ugprade to a better worker bot!\nNote: amount is calculated on the basis of recipe quantity and your input amount")
        
        # remove all ingredients from user's inventory
        for ingredient in required_ingredients:
            remove_item(ctx.author.id, ingredient, amount)

        add_active(ctx.author, recipe, quantity)
        i = 0
        while i <= quantity:
            await asyncio.sleep(workers[worker_bot][4])
            i += workers[worker_bot][5]

def setup(bot:commands.Bot):
    bot.add_cog(Workers(bot))
