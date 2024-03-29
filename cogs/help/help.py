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
from discord.ui import Button, View

from utils.help_pages import get_help_embed_pages


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='help',
        description='Don\'t know how to play? Looking for new commands? Then this is the command you\'re looking for.',
        usage='/help'
    )
    async def help(self, ctx:discord.ApplicationContext, page:discord.Option(int, required=True)):
        if page == 0:
            return await ctx.respond("There's no page number \"0\"!\nOnly pages 1-3 are there.")
        await ctx.defer()
        
        pages = get_help_embed_pages()

        await ctx.respond(embed=pages[page-1])


def setup(bot:commands.Bot):
    bot.add_cog(Help(bot))