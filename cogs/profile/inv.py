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
        
        user_data = get_user_data(ctx.author.id)


        class Dropdown(discord.ui.Select):
            def __init__(self, bot_: discord.Bot):
                self.bot = bot_
                
                options = [
                            discord.SelectOption(label="Ingredients", description="View your ingredients", emoji="🧂"),
                            discord.SelectOption(label="Cooking", description="View dishes being currently cooked", emoji="🍳"),
                            discord.SelectOption(label="Ready", description="View dishes that are prepared", emoji="🍰"),
                            discord.SelectOption(label="Cancel", description="Exit", emoji="❌"),
                        ]

                super().__init__(
                    placeholder="Choose inventory mode:",
                    min_values=1,
                    max_values=1,
                    options=options,
                )

            async def callback(self, interaction: discord.Interaction):
                if self.values[0] == 'Cancel':
                    return await interaction.response.send_message("Exited.")
                elif self.values[0] == 'Ingredients':
                    inv = user_data['inv'].items()
                    
                    if not bool(inv) or len(inv) < 0:
                        await interaction.response.send_message("No ingredients in your inventory!")
 
                    embed = discord.Embed(
                        title='Ingredient List',
                        description='These are your ingredients:',
                        color=discord.Colour.teal()
                    )

                    for x in inv:
                        data = get_shop_data(x[0])
                        
                        embed.add_field(
                            name=f'{data[1][2]} {data[0]} - {x[1]}',
                            value=f'Id: `{data[1][0]}`',
                            inline=False
                        )

                    await interaction.response.send_message(embed=embed)

                elif self.values[0] == 'Cooking':
                    active = user_data['active'].items()
                    
                    if not bool(active) or len(active) < 0:
                        await interaction.response.send_message("No dishes currently being prepared!")
                        
                    embed = discord.Embed(
                        title='Active List',
                        description='These are dishes being cooked:',
                        color=discord.Colour.teal()
                    )
                    
                    for x in active:
                        data = get_menu_data(x[0])

                        embed.add_field(
                            name=f'{data[1][3]} {data[0]} - `x{x[1]}`',
                            value=f'Id: {data[1][0]}'
                        )
                    
                    await interaction.response.send_message(embed=embed)
                    
                elif self.values[0] == 'Ready':
                    dishes = user_data['dishes'].items()
                    
                    if not bool(dishes) or len(dishes) < 0:
                        await interaction.response.send_message("No dishes currently being prepared!")
                        
                    embed = discord.Embed(
                        title='Ready Food List',
                        description='These are dishes being cooked:',
                        color=discord.Colour.teal()
                    )
                    
                    for x in dishes:
                        data = get_menu_data(x[0])

                        embed.add_field(
                            name=f'{data[1][3]} {data[0]} - `x{x[1]}`',
                            value=f'Id: `{data[1][0]}`'
                        )

                    await interaction.response.send_message(embed=embed)
                
        class DropdownView(discord.ui.View):
            def __init__(self, bot_: discord.Bot):
                self.bot = bot_
                super().__init__(Dropdown(self.bot), timeout=15)

            async def on_timeout(self):
                for child in self.children:
                    child.disabled = True
                await self.message.edit(content="You took too long! Disabled all the components.", view=self)


        view = DropdownView(self.bot)
        
        embed = discord.Embed(
            title='Inventory',
            description='Select your option from the dropdown menu',
            color=discord.Colour.teal()
        )
        await ctx.respond(embed=embed, view=view)

   
def setup(bot:commands.Bot):
    bot.add_cog(Inventory(bot))