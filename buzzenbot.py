#!/usr/bin/env python3

import discord
from discord import *

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True 

# -------------------------------------
path_to_token = "./.token"
# -------------------------------------

client = discord.Client(intents=intents)

token = ""
with open(path_to_token, "r", encoding="utf8") as f:
    token = f.read().splitlines()[0]


# The bot will send its message for reactions into this channel id
reaction_message_channel_id: str = "1244337390667956295"
reaction_message_channel: TextChannel = None

# Emoji -> role which is given when reacting with the emoji
emoji_role_map: dict = {
    "🇬🇧": "EN",
    "🇩🇪": "DE",
    "⚔️": "Clan War Participant",
    "🛡️": "Clan War Reservist"
}

# building the message which will be sent to be reacted to 
reaction_message_content: str = "React to this message to receive the roles you want:"

for emoji in emoji_role_map.keys():
    reaction_message_content += "\n"
    reaction_message_content += emoji + " : " + emoji_role_map[emoji]


@client.event
async def on_ready():
    reaction_message_channel = await client.fetch_channel(reaction_message_channel_id)
    await reaction_message_channel.send(reaction_message_content)

    print(f"Logged in as {client.user}.")


@client.event
async def on_message(message: Message):
    if message.author != client.user: # not adding reactions to foreign messages
        return
    
    # adding reaction to the message which was sent in on_ready
    for emoji in emoji_role_map.keys():
        await message.add_reaction(emoji)

@client.event
async def on_reaction_add(reaction: Reaction, user: User) -> None:
    if reaction.message.author != client.user: # not reacting to foreign messages
        return
    if user == client.user: # not reacting to the bots own reaction
        return
    
    # checking if reaction emoji is configured in our dict
    role_name = emoji_role_map[str(reaction.emoji)]
    if not role_name:
       return
    
    # checking if configured role from dict exists on the server
    guild = reaction.message.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        return

    # granting role
    await user.add_roles(role)
    print("Gave role " + role.name + " to " + user.name)

@client.event
async def on_reaction_remove(reaction: Reaction, user: User) -> None:
    if reaction.message.author != client.user: # not reacting to foreign messages
        return
    if user == client.user: # not reacting to the bots own reaction
        return

    # checking if reaction emoji is configured in our dict
    role_name = emoji_role_map[str(reaction.emoji)]
    if not role_name:
       return

    # checking if configured role from dict exists on the server
    guild = reaction.message.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        return

    # removing role
    await user.remove_roles(role)
    print("Removed role " + role.name + " from " + user.name)

client.run(token)
