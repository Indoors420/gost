import discord, dotenv, os
import coinmarketcap_api
import bot_commands
from discord.ext import commands


dotenv.load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix="~")

# Reply to message in previous channel
async def reply_message(prev_msg, new_msg):
    print(f"Replying to message in {prev_msg.channel} : {new_msg}")
    await prev_msg.channel.send(new_msg)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    new_msg = bot_commands.check_message(message)
    if new_msg != None:
        print(f"Guilds: {client.guilds}")
        print(f"{message.author} : {message.content}")
        await reply_message(message, new_msg)


client.run(token)
