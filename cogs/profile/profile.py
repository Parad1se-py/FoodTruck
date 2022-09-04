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


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='profile',
        description='View another player\'s profile.',
        usage='/profile <member>'
    )
    async def profile(self,
                      ctx: discord.ApplicationContext,
                      member : Option(discord.Member, required=False)=None):
        if not member:
            member = ctx.author
        if not check_acc(member.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        data = get_user_data(member.id)
        badges = ' '.join(data['badges'])

        profile_embed = discord.Embed(
            title=f"{ctx.author.name}'s profile",
            description=badges,
            color=discord.Colour.gold()
        )
        profile_embed.add_field(
            name="Cash:",
            value=f"`${data['cash']}`",
            inline=False
        )
        profile_embed.add_field(
            name="XP:",
            value=f"`{data['level']}`/`{data['level_l']}`",
            inline=False
        )
        profile_embed.set_thumbnail(url=ctx.author.avatar.url)

        return await ctx.respond(embed=profile_embed)
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name='balance',
        description='View your or another player\'s balance.',
        usage='/balance <member>'
    )
    async def bal(self,
                      ctx: discord.ApplicationContext,
                      member : Option(discord.Member, required=False)=None):
        if not member:
            member = ctx.author
        if not check_acc(member.id):
            return await ctx.respond("This user doesn't have a profile as they haven't played yet!")

        data = get_user_data(member.id)    
        
        bal_embed = discord.Embed(
            title='Total cash',
            description='You currently have `$' + str(data['cash']) + '`.',
            color=discord.Colour.teal()
        )

        return await ctx.respond(embed=bal_embed)

    
def setup(bot:commands.Bot):
    bot.add_cog(Profile(bot))
