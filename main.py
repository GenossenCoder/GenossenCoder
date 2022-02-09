from http import client
from TOKEN import TOKEN
from discord import *
import asyncio

INDIC = ">"


client = Client()


async def handle_server_msg(message):
    await handle_admin_cmd(message)


    for r in message.author.roles:
        if r.id == 773996048094986241 or r.id == 773993684651212812:
            await handle_admin_cmd(message)

async def handle_admin_cmd(message):
    cmd: str = message.content.replace(INDIC, "")

    if cmd == "help":
        await message.channel.send("Command to create new poll: \n '>new [Option 1, Option 2, usw.] \"Text describing the vote.\" x' where x is the length in hours the poll should run")

    elif cmd.startswith("new"):
        splitted = cmd.split("\"")
        text = splitted[1]
        hours = splitted[2].strip()
        options = cmd[cmd.find("[")+1 : cmd.find("]")]
        # neue wahl

    elif cmd.startswith("running"):
        # print laufenden wahlen
        pass

    elif cmd.startswith("delete"):
        poll_id = cmd.split(" ")[1]

@client.event
async def on_message(message):
    author: Member = message.author

    if author == client.user:
        return

    if not message.content.startswith(INDIC):
        return

    # private channel
    if str(message.channel.type) == "private":
        await message.channel.send("hure")
    # server
    else:
        await handle_server_msg(message)

                


client.run(TOKEN)