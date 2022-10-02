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
from data import *

class Recipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_menu_list = [x for x, y in menu.items()]

    async def item_searcher(self, ctx: discord.AutocompleteContext):
        return [item for item in self.loaded_menu_list if item.startswith(ctx.value.lower())]
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='recipe',
        description='Grab the recipe of any dish on the menu!',
        usage='/recipe [dish ID/name]'
    )
    async def recipe(
        self,
        ctx: discord.ApplicationContext,
        dish: Option(str, description='The ID/name of the dish you want to fetch the recipe of.', autocomplete=item_searcher)
    ):
        if not check_acc(ctx.author.id):
            return await ctx.respond("You don't have an account as you haven't played yet! Start with `/daily`!")
        
        await ctx.defer()
        
        for key, value in menu.items():
            if dish.lower() in [key.lower(), value[0]]:
                ingredients = ', '.join(value[1])
                
                recipe_embed = discord.Embed(
                    title=f"{value[3]} {key}'s Recipe",
                    description=f"The ingredients required are: **{ingredients}**",
                    color=discord.Colour.teal()
                )
                recipe_embed.set_footer(text=f"Use `/cook {value[0]}` to prepare this meal!")
                
                return await ctx.respond(embed=recipe_embed)
        
        await ctx.respond("No such dish!")


def setup(bot:commands.Bot):
    bot.add_cog(Recipe(bot))
