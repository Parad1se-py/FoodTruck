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


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.slash_command(
        name='inventory',
        description='View your inventory',
        usage='/inventory'
    )
    async def inventory(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        user_acc = check_acc(ctx.author.id)
        if not check_acc(ctx.author.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        class DropdownView(discord.ui.View):
            def __init__(self, bot_: discord.Bot):
                self.bot = bot_
                super().__init__(timeout=15)

            async def on_timeout(self):
                for child in self.children:
                    child.disabled = True
                await msg.edit(content="Dropdown has been disabled, since you didn't answer (again/at all) within time limit.", view=self)
                
            @discord.ui.select(
                options = [
                            discord.SelectOption(label="Ingredients", description="View your ingredients", emoji="🧂"),
                            discord.SelectOption(label="Cooking", description="View dishes being currently cooked", emoji="🍳"),
                            discord.SelectOption(label="Ready", description="View dishes that are prepared", emoji="🍰"),
                            discord.SelectOption(label="Cancel", description="Exit", emoji="❌"),
                        ],
                placeholder="Choose inventory mode:",
                min_values=1,
                max_values=1
            )
            async def _callback(self, select, interaction):
                if select.values[0] == 'Cancel':
                    for child in self.children:
                        child.disabled = True
                    return await msg.edit("Cancelled.", view=self)

                elif select.values[0] == 'Ingredients':
                    await interaction.response.send_message(embed=get_ing_embed(ctx.author.id))

                elif select.values[0] == 'Cooking':
                    await interaction.response.send_message(embed=get_active_embed(ctx.author.id))

                elif select.values[0] == 'Ready':
                    await interaction.response.send_message(embed=get_ready_embed(ctx.author.id))


        view = DropdownView(self.bot)

        embed = discord.Embed(
            title='Inventory',
            description='Select your option from the dropdown menu',
            color=discord.Colour.teal()
        )
        msg = await ctx.respond(embed=embed, view=view)

   
def setup(bot:commands.Bot):
    bot.add_cog(Inventory(bot))