# Work with Python 3.6
import discord
import json
import rinabot

with open('config.json') as file:
    file = json.load(file)

TOKEN = file['token']
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        messageCore = str(message.content).strip('!')
        reply = rinabot.reply(messageCore)
        await message.channel.send(reply)


@client.event
async def on_ready():
    print('------')
    print('Logged in as', client.user.name, client.user.id)
    print('------')


rinabot = rinabot.Bot(train=True)
client.run(TOKEN)   