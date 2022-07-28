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

from data import *
from utils.db import get_user_data


def get_ing_embed(id):
    embed = discord.Embed(
        title='Ingredients Inventory',
        color=discord.Colour.teal()
    )
    
    user_data = get_user_data(id)
    inv = user_data['inv'].items()
    
    if len(inv) <= 0:
        embed.description = 'You currently have no ingredients in your inventory!'
    else:
        embed.description = 'These are your ingredients:'
    
    for x in inv:
        for key, value in ing_shop.items():
            if x[0] == value[0]:
                embed.add_field(
                    name=f'{value[2]} {key} - {x[1]}',
                    value=f'Id: `{value[0]}`',
                    inline=False
                )
    
    return embed

def get_active_embed(id):
    embed = discord.Embed(
        title='Being-cooked Food List',
        color=discord.Colour.teal()
    )

    user_data = get_user_data(id)
    dishes = user_data['active'].items()
    
    if len(dishes) <= 0:
        embed.description = 'You don\'t have any dishes currently being cooked!'
    else:
        embed.description = 'These are the dishes being cooked: '

    for x in dishes:
        for key, value in menu.items():
            if x[0] == value[0]:
                embed.add_field(
                    name=f'{value[3]} {key} - `x{x[1]}`',
                    value=f'Id: {value[0]}'
                )
                
    return embed

def get_ready_embed(id):
    embed = discord.Embed(
        title='Ready-to-serve Food List',
        color=discord.Colour.teal()
    )

    user_data = get_user_data(id)
    dishes = user_data['dishes'].items()
    
    if len(dishes) <= 0:
        embed.description = 'You don\'t have any dishes that are cooked!'
    else:
        embed.description = 'These are the dishes that are ready-to-serve: '
    
    for x in dishes:
        for key, value in menu.items():
            if x[0] == value[0]:
                embed.add_field(
                    name=f'{value[3]} {key} - `x{x[1]}`',
                    value=f'Id: {value[0]}'
                )
                
    return embed

def get_lootboxes_embed(id):
    embed = discord.Embed(
        title='Ready-to-serve Food List',
        color=discord.Colour.teal()
    )

    user_data = get_user_data(id)
    lootbox = user_data['lootboxes'].items()
    
    if len(lootbox) <= 0:
        embed.description = 'You don\'t have any lootboxes in your inventory.'
    else:
        embed.description = 'These are your ready-to-loot looboxes: '
        
    for x in lootbox:
        for key, value in lootboxes.items():
            if x[0] == value[0]:
                embed.add_field(
                    name=f'{value[3]} {key} - `x{x[1]}`',
                    value=f'Id: {value[0]}'
                )

    return embed