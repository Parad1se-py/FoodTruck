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


def get_page_1() -> discord.Embed:
    page_1 = discord.Embed(
        title='Help Menu',
        description='If you\'re new, get started with `/start`!',
        color=discord.Colour.teal()
    )
    page_1.add_field(
        name='`/daily`',
        value='Get your daily freebies! | Cooldown: `24h 0m 0s`',
        inline=False
    )
    page_1.add_field(
        name='`/help`',
        value='Displays this command you\'re seeing right now. | Cooldown: `5s`',
        inline=False
    )
    page_1.add_field(
        name='`/profile <user>`',
        value='Displays your/user\'s FoodTruck profile. | Cooldown: `5s`',
        inline=False
    )
    page_1.add_field(
        name='`/balance`',
        value='View how much cash you got! | Cooldown: `5s`',
        inline=False
    )
    page_1.add_field(
        name='`/inventory`',
        value='View your dishes, cooking, ingredients and lootboxes! | Cooldown: `7s`',
        inline=False
    )
    page_1.add_field(
        name='`/start`',
        value='New to FoodTruck? Use this command and open an account & freebies! | One-time use',
        inline=False
    )
    
    return page_1

def get_page_2() -> discord.Embed:
    page_2 = discord.Embed(
        title='Help Menu',
        description='If you\'re new, get started with `/start`!',
        color=discord.Colour.teal()
    )
    page_2.add_field(
        name='`/shop`',
        value='View the shop! | Cooldown: `5s`',
        inline=False
    )
    page_2.add_field(
        name='`/buy [item-id] <amount>`',
        value='Buy an item from the shop. | Cooldown: `5s`',
        inline=False
    )
    page_2.add_field(
        name='`/menu`',
        value='View the menu! | Cooldown: `5s`',
        inline=False
    )
    page_2.add_field(
        name='`/recipe [dish-id]`',
        value='View the recipe of a particular dish! | Cooldown: `5s`',
        inline=False
    )
    page_2.add_field(
        name='`/cook [item-id] <amount>`',
        value='Cook an item that is available on the menu! | Cooldown: `5s`',
        inline=False
    )
    page_2.add_field(
        name='`/serve [item-id] <amount>`',
        value='Serve an item in your inventory to customers! | Cooldown: `3s`',
        inline=False
    )
    
    return page_2

def get_page_3() -> discord.Embed:
    page_3 = discord.Embed(
        title='Help Menu',
        description='If you\'re new, get started with `/start`!',
        color=discord.Colour.teal()
    )
    page_3.add_field(
        name='`/leaderboard global`',
        value='View the global leaderboard! | Cooldown: `15s`',
        inline=False
    )
    page_3.add_field(
        name='`/leaderboard server`',
        value='View the server leaderboard! | Cooldown: `15s`',
        inline=False
    )
    page_3.add_field(
        name='`/lootboxes`',
        value='View all the lootboxes from FoodTruck. | Cooldown: `5s`',
        inline=False
    )
    page_3.add_field(
        name='`/lootbox info [lootbox-id]`',
        value='Get information about a particular lootbox. | Cooldown: `3s`',
        inline=False
    )
    page_3.add_field(
        name='`/lootbox buy [lootbox-id] <amount>`',
        value='Buy a lootbox to open for rewards! | Cooldown: `3s`',
        inline=False
    )
    page_3.add_field(
        name='`/lootbox open [lootbox-id] <amount>`',
        value='Open a lootbox that you have! | Cooldown: `5s`',
        inline=False
    )
    
    return page_3

def get_page_4() -> discord.Embed:
    page_4 = discord.Embed(
        title='Help Menu',
        description='If you\'re new, get started with `/start`!',
        color=discord.Colour.teal()
    )
    page_4.add_field(
        name='`/slots [bet]`',
        value='Gamble your cash on the slots machine! | Cooldown: `15s`',
        inline=False
    )
    page_4.add_field(
        name='`/bet [bet]`',
        value='Bet your money, see who gets the highest strike! | Cooldown: `10s`',
        inline=False
    )
    page_4.add_field(
        name='`/cup [bet]`',
        value='Guess which cup has a candy under it! | Cooldown: `15s`',
        inline=False
    )
    page_4.add_field(
        name='`/lootbox info [lootbox-id]`',
        value='Get information about a particular lootbox. | Cooldown: `3s`',
        inline=False
    )
    page_4.add_field(
        name='`/lootbox buy [lootbox-id] <amount>`',
        value='Buy a lootbox to open for rewards! | Cooldown: `3s`',
        inline=False
    )
    page_4.add_field(
        name='`/lootbox open [lootbox-id] <amount>`',
        value='Open a lootbox that you have! | Cooldown: `5s`',
        inline=False
    )
    
    return page_4

def get_help_embed_pages() -> list:
    return [get_page_1(), get_page_2(), get_page_3(), get_page_4]
