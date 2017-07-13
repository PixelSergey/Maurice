#!/usr/bin/python3

import discord
from discord.ext import commands
import asyncio
import sys
import os
import glob
import aiohttp
import json
import datetime

settings = {}
prefix = ""
desc = ""
joinsound = ""
channel = {}

if not discord.opus.is_loaded():
    print("Could not load the opus library; terminating")
    sys.exit()


def read_settings():
    os.chdir(sys.path[0])
    with open("settings.json", "r") as settings_file:
        global settings 
        global prefix
        global desc
        global joinsound
        
        settings = json.load(settings_file)
        prefix = settings["prefix"]
        desc = settings["desc"]
        joinsound = settings["joinsound"]


def print_settings():
    print("Prefix: " + prefix + "\tdesc: " + desc)


def set_bot_settings():
    bot.command_prefix = commands.when_mentioned_or(prefix)
    bot.description = desc


def update_game():
    yield from bot.change_presence(game=discord.Game(name="Use me: " + prefix + "help"))

read_settings()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), description=desc)


@bot.event
@asyncio.coroutine
def on_ready():    
    yield from update_game()
    print("------")    
    print_settings()
    print("------")
    print(datetime.datetime.now())
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
@asyncio.coroutine
def on_server_join(server):
    msg = """Hello! :wave: My name is Maurice. Thanks for adding me to this server :smile:
You can use me for voice clips, responses and more!
Type {}help to find out more about my commands. Please test me out!
Made by Sergey:flag_fi:. Github link: https://github.com/PixelSergey/Maurice/""".format(prefix)
    yield from bot.send_message(server.default_channel, msg)


@bot.event
@asyncio.coroutine
def on_message(message):
    if message.author.bot:  # Do not respond to self or to other bots
        return
    if message.content[:5].lower() == "hello" or message.content[:2].lower() == "hi":
        msg = "Hello {0.author.mention}".format(message)
        yield from bot.send_message(message.channel, msg)
    if message.content[:4].lower() == "ping":
        yield from bot.send_message(message.channel, ":ping_pong:Pong!")

    yield from bot.process_commands(message)


@bot.command(aliases=["set", "settings"])
@asyncio.coroutine
def setting(setting="", *, value=""):
    """Modifies bot settings
    Valid settings are prefix and description"""
    if value == "":
        yield from bot.say("Invalid value, usage " + prefix + "settings <setting> <value>")
        return
    if not setting in list(settings.keys()): 
        yield from bot.say("Invalid setting, usage " + prefix + "settings <setting> <value>")
        return

    settings[setting] = value
    os.chdir(sys.path[0])
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4)

    read_settings()  # Update global variables
    set_bot_settings()  # Set written settings to the bot
    yield from update_game()  # Update command prefix for bot status if it was changed
    yield from bot.say("Updated settings!\n" + ', '.join('{}: {}'.format(key, val) for key, val in settings.items()))


@bot.command()
@asyncio.coroutine
def ping():
    """Pong!
    Yes, this is a test command"""
    yield from bot.say(":ping_pong:Pong!")


@bot.command(pass_context=True)
@asyncio.coroutine
def flip(ctx):
    """Flips the last sent line of text upside-down
    uʍop-ǝpᴉsdn ʇxǝʇ ɟo ǝuᴉl ʇuǝs ʇsɐl ǝɥʇ sdᴉlℲ"""
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
    yield from bot.say("Shutting down...")
    yield from bot.say("Bye")
    yield from bot.logout()


@bot.command(pass_context=True, no_pm=True)
@asyncio.coroutine
def summon(ctx):
    """Summons Maurice to your voice channel
    Must be in a voice channel to use."""
    summon_channel = ctx.message.author.voice_channel
    summon_server = ctx.message.server
    if summon_channel is None:
        yield from bot.say("You can't summon me if you're not in a channel!")
        return

    global channel
    if not summon_server in channel:
        channel[summon_server] = yield from bot.join_voice_channel(summon_channel)
    else:
        channel[summon_server].move_to(summon_channel)
    yield from bot.say("Summoned to channel " + channel[summon_server].channel.name + " successfully!")
    yield from ctx.invoke(play, clip_name=joinsound)


@bot.command(no_pm=True, pass_context=True, aliases=["kick"])
@asyncio.coroutine
def disconnect(ctx):
    """Disconnects Maurice from the voice channel"""
    global channel
    disconnect_server = ctx.message.server
    if not disconnect_server in channel:
        yield from bot.say("I wasn't connected in the first place")
        return
    
    yield from channel[disconnect_server].disconnect()
    del channel[disconnect_server]


@bot.command(aliases=["list"])
@asyncio.coroutine
def cliplist():
    """Lists all sound clips"""
    os.chdir(sys.path[0])
    yield from bot.say("Available sound clips: " + ", ".join([os.path.basename(f.strip(".mp3")) for f in glob.glob('audio/*.mp3')]))


@bot.command(pass_context=True, no_pm=True)
@asyncio.coroutine
def upload(ctx, filename=""):
    """Lets you upload a voice clip to the bot
    Upload a .mp3 file with the command to upload it"""
    if filename == "":
        yield from bot.say("Please insert a filename: usage (while uploading a file) " + prefix + "upload <filename>")
        return

    if " " in filename:
        yield from bot.say("The filename may not contain spaces!")
        return

    if len(ctx.message.attachments) != 1:
        yield from bot.say("You must attach one (and only one) .mp3 file to the command to upload it")
        return
    
    file = ctx.message.attachments[0]
    if not file["filename"].endswith(".mp3"):
        yield from bot.say("The file must be an .mp3 file!")
        return

    if file["size"] > 500000:
        yield from bot.say("The file cannot be over 500KB (roughly 10sec. high-quality .mp3)")
        return

    url = file["url"]
    
    try:
        session = aiohttp.ClientSession()
        with aiohttp.Timeout(10, loop=session.loop):
            try:
                response = yield from session.get(url)
                with open("audio/" + filename + ".mp3", 'wb') as fd:
                    while True:
                        chunk = yield from response.content.read()
                        if not chunk:
                              break
                        fd.write(chunk)
        
            finally:
                response.release()
    finally:
        session.close()
    
    yield from bot.say("Written file " + filename + ".mp3 successfully!")


@bot.command(pass_context=True)
@asyncio.coroutine
def download(ctx, filename=""):
    """Lets you download a clip"""
    if filename == "":
        yield from bot.say("You must enter a clip to download, usage: " + prefix + "download <filename>")
        return
    
    os.chdir(sys.path[0])
    yield from bot.send_file(ctx.message.channel, "audio/" + filename + ".mp3", content="Here's your file <3")


@bot.command(no_pm=True, pass_context=True)
@asyncio.coroutine
def play(ctx, clip_name=""):
    """Plays a sound clip"""
    play_server = ctx.message.server
    if not play_server in channel:
        yield from bot.say("I must be in a voice channel to play clips!")
        return
    if clip_name == "":
        yield from bot.say("Invalid clip name; usage " + prefix + "play <clip_name>")
    
    os.chdir(sys.path[0])
    channel[play_server].create_ffmpeg_player("audio/" + clip_name + ".mp3").start()


@bot.command(aliases=["respond"])
@asyncio.coroutine
def r(*, response=""):
    pass


@bot.command(pass_context=True)
@asyncio.coroutine
def response():
    pass


# Get key, initialize bot
os.chdir(sys.path[0])
with open("secret.key", "r") as secret:
    key = secret.readline().strip()

bot.run(key)

