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


def get_page(x, y) -> discord.Embed:
    embed = discord.Embed(
        title='Menu',
        description='You can cook these items using the cook command if you have achieved the required level: `/cook <item> [amount]`',
        color=discord.Colour.teal()
    )

    for i, (key, value) in enumerate(menu.items(), start=1):
        if i >= x:
            if i > y:
                return embed
            embed.add_field(
                name=f"{value[3]} {key} | Id: `{value[0]}`",
                value=f"`${value[6]}` | Makes `{value[2]}` | Level required: __`{value[4]}`__\n"\
                       f"**{', '.join(value[1])}**",
                inline=False
            )
    return embed

def get_menu_embed_pages() -> list:
    return [get_page(1, 6), get_page(7, 12)]
