#!/usr/bin/env python3

import discord

intents = discord.Intents.default()
intents.message_content = True

# -------------------------------------
prefix = "!"
path_to_token = "./.token"
# -------------------------------------

client = discord.Client(intents=intents)

token = ""
with open(path_to_token, "r", encoding="utf8") as f:
    token = f.read().splitlines()[0]


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.channel.name == "bot" or message.channel.name == "bot-befehle" or message.channel.id == 1091452282878562405:
        return

    args = message.content.split(" ")
    response = "Kein bekannter Befehl. Versuch mal " + prefix + "help, um Hilfe zu bekommen"

    if not args[0].startswith(prefix):
        return
    if args[0] == (prefix + 'ping'):
        response = "pong"

    await message.channel.send(response, reference=message)

client.run(token)
