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


class Lootbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_lootboxes_list = [x for x, y in lootboxes.items()]

    async def lootbox_searcher(self, ctx: discord.AutocompleteContext):
        return [lootbox for lootbox in self.loaded_lootboxes_list if lootbox.lower().startswith(ctx.value.lower()) or lootbox.lower() == ctx.value.lower()]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    lootbox_slash_group = discord.SlashCommandGroup('lootbox', description='All commands related to FoodTruck lootboxes!')
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='lootboxes',
        description='Get a list of all the lootboxes',
        usage='/lootboxes'
    )
    async def lootboxes(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        embed = discord.Embed(
            title='Lootboxes',
            colour=discord.Colour.teal()
        )
        
        for key, value in lootboxes.items():
            embed.add_field(
                name=f'{value[3]} {key} - `${value[1]}`',
                value=f'Id : `{value[0]}`'
            )
            
        return await ctx.respond(embed=embed)
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @lootbox_slash_group.command(
        name='info',
        description='View details of a lootbox',
        usage='/lootbox info [id/name]'
    )
    async def lootbox_info(self,
                           ctx: discord.ApplicationContext,
                           lootbox: Option(str, description='Pick a lootbox to view it\'s details.', autocomplete=lootbox_searcher)):
        await ctx.defer()

        for key, value in lootboxes.items():
            if lootbox.lower() == key.lower:
                possible_items = ', '.join(value[2])
                embed = discord.Embed(
                    title=f'{value[3]} {key}',
                    description=f'Cost: `${value[1]}`, Id: `{value[0]}`\nGives: **{possible_items}**',
                    colour=discord.Colour.teal()
                )
                embed.set_thumbnail(url=value[4])

                return await ctx.respond(embed=embed)

        return await ctx.respond("No such lootbox found! Try the command `/lootboxes` to view all lootboxes.")
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @lootbox_slash_group.command(
        name='open',
        description='Open FoodTruck lootboxes that you own.',
        usage='/lootbox open [id/name]'
    )
    async def lootbox_open(self,
                           ctx: discord.ApplicationContext,
                           name: Option(str, description='Pick a lootbox to open.', autocomplete=lootbox_searcher),
                           amount: Option(int, required=False)=1):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("You don't have a FoodTruck account yet! To get started, use `/start` or `/daily`!")
        
        if not check_for_lootbox(ctx.author.id, name):
            return await ctx.respond("You don't own that lootbox! Use `/inventory` to view lootboxes owned by you.\nView the lootbox shop using `/lootboxes`", ephemeral=True)
        count = lootbox_count(ctx.author.id, name)
        if count < amount:
            return await ctx.respond(f"You only have `{count}` {name} lootbox(es).", ephemeral=True)
        
        initial_embed = discord.Embed(
            title=f'Opening {name} lootbox...',
            colour=discord.Colour.teal()
        )

        msg = await ctx.respond(embed=initial_embed)
        await asyncio.sleep(1.5)
        
        remove_lootboxes(ctx.author.id, name, amount)
        
        final_embed = discord.Embed(
            title=f'{ctx.author.name}\'s {name} lootbox rewards...',
            description=f'You opened {name} lootbox and got:'
        )

        for reward in lootboxes[name][2]:
            if reward == 'cash':
                cash = calculate_cash(name)
                update_data(ctx.author.id, 'cash', cash*amount)
                final_embed.add_field(
                    name='Cash:',
                    value=f'`${cash}`',
                )
            elif reward == 'level':
                lvl = calculate_level(name)
                await update_l(ctx.author.id, lvl*amount)
                final_embed.add_field(
                    name='Exp points:',
                    value=f'`{lvl}`'
                )
            elif reward == 'ingredients':
                ings = calculate_ingredients(name)
                ings_list = []
                for key, value in ings.items():
                    add_item(ctx.author, key, value)
                    ings_list.append(f'{key}: x{value}')
                final_embed.add_field(
                    name='Ingredients:',
                    value=', '.join(ings_list)
                )
            elif reward == 'dish':
                dishes = calculate_dish(name)
                dishes_list = []
                for key, value in dishes.items():
                    add_dish(ctx.author, key, value)
                    dishes_list.append(f'{key}: x{value}')
                final_embed.add_field(
                    name='Dishes:',
                    value=', '.join(dishes_list)
                    )

        return await msg.edit(embed=final_embed)

    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @lootbox_slash_group.command(
        name='buy',
        description='Buy a lootbox from the store!',
        usage='/buy [loobox id/name] <amount>'
    )
    async def buy_lootbox(self,
                          ctx: discord.ApplicationContext,
                          name: Option(str, description='Pick a lootbox to buy.', autocomplete=lootbox_searcher),
                          amount: Option(int, required=False)=1):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("You don't have a FoodTruck account yet! To get started, use `/daily`!")

        if name not in lootboxes.keys():
            return await ctx.respond("No such lootbox! Use `/lootboxes` to get a list of all lootboxes.\nUse `/inventory` to view your owned lootboxes!")

        user_cash = get_user_data(ctx.author.id)['cash']
        price = lootboxes[name][1]*amount

        if price > user_cash:
            return await ctx.respond(f"You don't have enough cash (`${price}`) to buy this lootbox", ephemeral=True)

        update_data(ctx.author.id, 'cash', -(price))
        add_lootbox(ctx.author.id, name, amount)

        return await ctx.respond(
            embed = discord.Embed(
                title="Successful purchase!",
                description=f"You successfully bought `{amount}x` **{name}** lootbox for `${price}`!",
                colour=discord.Colour.teal()
            )
        )


def setup(bot:commands.Bot):
    bot.add_cog(Lootbox(bot))
