import discord
from discord.ext import commands
import asyncio

class System():
    def __init__(self, bot):
        self.bot = bot

    
    @bot.command(aliases=["sd"])
    @asyncio.coroutine
    def shutdown():
        """Shuts Maurice down"""
        yield from bot.say("Shutting down...")
        yield from bot.say("Bye :wave:")
        yield from bot.logout()


    


def setup(bot):
    bot.add_cog(System(bot))
