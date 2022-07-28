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
from data import lootbox_list

from utils import *
from data import *


class Lootbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='lootboxes',
        description='Get a list of all the lootboxes',
        usage='/lootboxes'
    )
    async def lootboxes(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        embed = discord.Embed(
            title='Lootboxes',
            color=discord.Colour.teal()
        )
        
        for key, value in lootboxes.items():
            embed.add_field(
                name=f'{value[3]} {key} - `${value[1]}`',
                value=f'Id : `{value[0]}`'
            )
            
        return await ctx.respond(embed=embed)
        
    @commands.slash_command(
        name='lootbox',
        description='View details of a lootbox',
        usage='/lootbox [id/name]'
    )
    async def lootbox_info(self,
                           ctx: discord.ApplicationContext,
                           lootbox: Option(str, required=True)):
        await ctx.defer()

        for key, value in lootboxes.items():
            if lootbox.lower() in [key.lower, value[0]]:
                possible_items = ', '.join(value[2])
                embed = discord.Embed(
                    title=f'{value[3]} {key}',
                    description=f'Cost: `${value[1]}`, Id: `{value[0]}`\nGives: **{possible_items}**'
                )
                embed.set_thumbnail(url=value[4])

                return await ctx.respond(embed=embed)

        return await ctx.respond("No such lootbox found! Try the command `/lootboxes` to view all lootboxes.")

def setup(bot:commands.Bot):
    bot.add_cog(Lootbox(bot))