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
    
    if message.content.startswith('-close'):
        # close connection
        await client.close()

    if message.content.startswith('-'):
        mes = message.content.strip('-')
        chat_reply = rinabot.reply(mes)
        if chat_reply != -1:
            await message.channel.send(chat_reply)
        else:
            return


@client.event
async def on_ready():
    print('-----------------------------------------------')
    print('Logged in as', client.user.name, client.user.id)
    print('-----------------------------------------------')


rinabot = rinabot.Bot(train=True, printInfo=True, shop_name="bunshopz")
client.run(TOKEN)   