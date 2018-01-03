import os
import discord

client = discord.Client()

hotwords = [
    'tit',
    'tits',
    'titty',
    'titties'
]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(msg):
    if any(word in msg.content.lower() for word in hotwords):
        await client.send_file(msg.channel, 'thetits.png')

    if 'ranch' in msg.content.lower():
        await client.send_file(msg.channel, 'cheers.jpg')

client.run(os.environ["bot_token"])
