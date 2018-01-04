import os
import discord
import re

client = discord.Client()

hotwords = [
    re.compile('\\btit\\b'),
    re.compile('\\btits\\b'),
    re.compile('\\btitty\\b'),
    re.compile('\\btitties\\b')
]

# TODO: use regex to not match words in words

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(msg):
    if any(re.search(regex, msg.content.lower()) for regex in hotwords):
        await client.send_file(msg.channel, 'thetits.png')

    if 'ranch' in msg.content.lower():
        await client.send_file(msg.channel, 'cheers.jpg')

client.run(os.environ["bot_token"])
