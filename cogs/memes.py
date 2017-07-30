import discord
from discord.ext import commands
import asyncio

class Memes():
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(pass_context=True)
    @asyncio.coroutine
    def flip(self, ctx):
        """Flips the last sent line of text upside-down
        uʍop-ǝpᴉsdn ʇxǝʇ ɟo ǝuᴉl ʇuǝs ʇsɐl ǝɥʇ sdᴉlℲ"""
        msg = yield from self.bot.logs_from(ctx.message.channel, limit=2)
        msg = list(msg)[1].content[::-1]
        real = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890<>\"'()[]{}?¿.,!¡&"
        flipped = "∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎzƖᄅƐㄣϛ9ㄥ860><„,)(][}{¿?˙'¡!⅋"
        tbl = str.maketrans(real, flipped)
        msg = msg.translate(tbl)
        yield from self.bot.say(msg)


    @commands.command()
    @asyncio.coroutine
    def ping(self):
        """Pong!
        Yes, this is a test command"""
        yield from self.bot.say(":ping_pong:Pong!")


def setup(bot):
    bot.add_cog(Memes(bot))
