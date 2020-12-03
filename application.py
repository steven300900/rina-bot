# Work with Python 3.6
import discord
import json
import rinabot
import learn

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

    if message.content == 'join':
        await discord.VoiceChannel.connect(message.author.voice.channel)

    if message.content.startswith('find'):
        query = message.content[4:]
        await message.channel.send(learn.find_video(query))

@client.event
async def on_ready():
    print('-----------------------------------------------')
    print('Logged in as', client.user.name, client.user.id)
    print('-----------------------------------------------')


rinabot = rinabot.Bot(train=False)
client.run(TOKEN)   