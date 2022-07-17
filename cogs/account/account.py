import discord
from discord import guild_only, slash_command
from discord.ext import commands
from discord.commands import slash_command, Option

class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    @guild_only()
    @slash_command(
        name='profile',
        usage='/profile <member>',
        description='View your or someone else\'s profile'
    )
    async def profile(self, ctx, member : Option(discord.member, required=False)=None):
        if not member:
            member = ctx.author
            
        ...