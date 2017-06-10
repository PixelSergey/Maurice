#!/usr/bin/python3

import discord
from discord.ext import commands
import asyncio
import sys
import os

prefix = "."
desc = ""


def readSettings():
    os.chdir(sys.path[0])
    with open("bot.settings", "r") as settings:
        global prefix
        global desc
        prefix = settings.readline().strip()
        desc = settings.readline().strip()


def printSettings():
    print("Prefix: " + prefix + "\tdesc: " + desc)

readSettings()
printSettings()
print("------")

bot = commands.Bot(command_prefix=prefix, description=desc)
bot.change_presence(game=discord.Game(name="use me"))


@bot.event
@asyncio.coroutine
def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command(pass_context=True)
@asyncio.coroutine
def mhelp(ctx):
    yield from bot.say("I do not yet have a help page")


@bot.command()
@asyncio.coroutine
def settings(setting="", *, value=""):
    if value == "":
        yield from bot.say("Invalid setting, usage " + prefix + "settings <prefix|desc> <value>")
        return
    if setting == "prefix":
        bot.command_prefix = value
        mode = 0
    elif setting == "desc" or setting == "description":
        bot.description = value
        mode = 1
    else:
        yield from bot.say("Invalid setting, usage " + prefix + "settings <prefix|desc> <value>")
        return

    os.chdir(sys.path[0])
    lines = []
    with open("bot.settings", "r+") as settings:
        lines = settings.readlines()
        lines[mode] = value + "\n"
        settings.seek(0)
        settings.truncate()
        for line in lines:
            settings.write(line)

    readSettings()  # Update global variables
    yield from bot.say("Updated settings!\nPrefix: " + prefix + "\nDescription: " + desc)


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
with open("secret.key", "r") as secret:
    key = secret.readline().strip()

bot.run(key)

