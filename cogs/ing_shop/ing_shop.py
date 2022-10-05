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
from discord.ext import commands, pages
from discord.commands import Option

from utils import *
from data import *


class Ingredients_Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_ingredient_list = [x for x, y in ing_shop.items()]

    async def item_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_ingredient_list if item.startswith(ctx.value.lower()) or item.lower() == ctx.value.lower()]
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='shop',
        description='View the ingredients shop!',
        usage='/shop'
    )
    async def shop(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        paginator = pages.Paginator(
            pages = get_shop_embed_pages(),
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=True,
            loop_pages=True,
            disable_on_timeout=True,
            timeout=15
        )
        await paginator.respond(ctx.interaction, ephemeral=False)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='buy',
        description='Buy an ingredient from the shop `/shop`',
        usage='/buy [item] <amount>'
    )
    async def buy(self,
                  ctx: discord.ApplicationContext,
                  item: Option(str, required=True, autocomplete=item_searcher),
                  amount: Option(int, requried=False)=1):
        await ctx.defer()

        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        user_data = get_user_data(ctx.author.id)

        for key, value in ing_shop.items():
            if item in [key, value[0]]:
                if ( amount * value[1] ) > user_data['cash']:
                    return await ctx.respond(f"You don't have enough money (`${amount*value[1]}`) to buy {item}!")
                add_item(ctx.author, item, amount)
                update_data(ctx.author.id, 'cash', -int(value[1]*amount))
                await update_l(ctx.author.id, 3*amount)
                success_embed = discord.Embed(
                    title="Successful Purchase",
                    description=f'You successfully bought `{amount}`x {value[2]} {key} for `${amount*value[1]}`!',
                    color=discord.Colour.teal()
                )
                success_embed.set_footer(text='Thanks for your purchase! Happy cooking :)')

                return await ctx.respond(embed=success_embed)
        await ctx.respond("No such ingredient in the shop!")

def setup(bot:commands.Bot):
    bot.add_cog(Ingredients_Shop(bot))
