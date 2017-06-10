import discord
from discord.ext import commands
import asyncio
import sys
import os

bot = commands.Bot(command_prefix="m!", description="A very interesting bot")


@bot.event
@asyncio.coroutine
def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
@asyncio.coroutine
def ping():
    yield from bot.say("Pong!")


@bot.command(pass_context=True)
@asyncio.coroutine
def flip(ctx):
    msg = yield from bot.logs_from(ctx.message.channel, limit=2)
    msg = list(msg)[1].content[::-1]
    real = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890<>\"'()[]{}?¿.,!¡&"
    flipped = "∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎzƖᄅƐㄣϛ9ㄥ860><„,)(][}{¿?˙'¡!⅋"
    tbl = str.maketrans(real, flipped)
    msg = msg.translate(tbl)
    yield from bot.say(msg)


@bot.command()
@asyncio.coroutine
def shutdown():
    yield from bot.say("Shutting down Maurice...")
    yield from bot.say("Bye")
    yield from bot.logout()


@bot.event
@asyncio.coroutine
def on_message(message):
    if message.author == bot.user:  # Do not respond to self
        return
    if message.content.startswith("hello") or message.content.startswith("hi"):
        msg = "Hello {0.author.mention}".format(message)
        yield from bot.send_message(message.channel, msg)
    yield from bot.process_commands(message)
    if message.content.startswith("ping"):
        yield from bot.send_message(message.channel, "Pong!")


# Get key, initialize bot
os.chdir(sys.path[0])
secret = open("secret.key", "r")
key = secret.readline().strip()
secret.close()

bot.run(key)

