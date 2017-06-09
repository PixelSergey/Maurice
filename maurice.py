import discord
import asyncio

client = discord.Client()

@client.event
@asyncio.coroutine
def on_message(message):  
    if message.author == client.user:
        return
    if message.content.startswith("hello") or message.content.startswith("hi"):
        msg = "Hello {0.author.mention}".format(message)
        yield from client.send_message(message.channel, msg)

@client.event
@asyncio.coroutine
def on_ready():  
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

secret = open("secret.key", "r")
key = secret.readline().strip()
secret.close()

client.run(key)
