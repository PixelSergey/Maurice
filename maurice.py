#!/usr/bin/python3

import discord
from discord.ext import commands
import asyncio
import sys
import os

prefix = "."
desc = ""
channel = None

if not discord.opus.is_loaded():
    print("Could not load the opus library; terminating")
    sys.exit()


def read_settings():
    os.chdir(sys.path[0])
    with open("bot.settings", "r") as settings:
        global prefix
        global desc
        prefix = settings.readline().strip()
        desc = settings.readline().strip()


def print_settings():
    print("Prefix: " + prefix + "\tdesc: " + desc)


def update_game():
    yield from bot.change_presence(game=discord.Game(name="Use me: " + prefix + "help"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), description=desc)


@bot.event
@asyncio.coroutine
def on_ready():
    read_settings()
    print_settings()
    yield from update_game()
    print("------")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command(aliases=["set"])
@asyncio.coroutine
def settings(setting="", *, value=""):
    """Modifies bot settings
    Valid settings are prefix and description"""
    if value == "":
        yield from bot.say("Invalid setting, usage " + prefix + "settings <prefix|desc> <value>")
        return
    if setting == "prefix":
        bot.command_prefix = commands.when_mentioned_or(value)
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

    read_settings()  # Update global variables
    yield from update_game()  # Update command prefix if it was changed
    yield from bot.say("Updated settings!\nPrefix: " + prefix + "\nDescription: " + desc)


@bot.command()
@asyncio.coroutine
def ping():
    """Pong!
    Yes, this is a test command"""
    yield from bot.say("Pong!")


@bot.command(pass_context=True)
@asyncio.coroutine
def flip(ctx):
    """Flips the last sent line of text upside-down"""
    msg = yield from bot.logs_from(ctx.message.channel, limit=2)
    msg = list(msg)[1].content[::-1]
    real = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890<>\"'()[]{}?¿.,!¡&"
    flipped = "∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎzƖᄅƐㄣϛ9ㄥ860><„,)(][}{¿?˙'¡!⅋"
    tbl = str.maketrans(real, flipped)
    msg = msg.translate(tbl)
    yield from bot.say(msg)


@bot.command(aliases=["sd"])
@asyncio.coroutine
def shutdown():
    """Shuts Maurice down"""
    yield from bot.say("Shutting down Maurice...")
    yield from bot.say("Bye")
    yield from bot.logout()


@bot.command(pass_context=True, no_pm=True)
@asyncio.coroutine
def summon(ctx):
    """Summons Maurice to your voice channel
    Must be in a voice channel to use."""
    summon_channel = ctx.message.author.voice_channel
    if summon_channel is None:
        yield from bot.say("You can't summon me if you're not in a channel!")
        return
    global channel
    channel = yield from bot.join_voice_channel(summon_channel)


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

