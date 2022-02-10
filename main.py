from TOKEN import TOKEN
from discord import *
from pie_chart import make_piechart
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from Database import *
import os

INDIC = ">"
client = Client()


async def send_as_piechart(id, channel_id):            
    poll = getPoll(id)

    votes = []
    for i in poll["competitors"]:
        votes.append(len(poll[i]))

    make_piechart(poll["competitors"], votes)

    with open("pie.png", "rb") as f:
        f = File(f)
        await client.get_channel(channel_id).send(file=f)
        f.close()    

@tasks.loop(hours=12)
async def send_chart():
    if running() == None:
       return
    else:
        for i in running():
            send_as_piechart(i)
        
async def handle_private_msg(message):
    cmd: str = message.content.replace(INDIC, "")

    # if cmd.startswith("show"):
    #     x = 0
    #     for i in running():
    #         x += 1
    #         send_as_piechart(i)
    #         await message.channel.send(getPoll(i))

            # hier nachricht vom user awaiten und dann add_vote aufrufen

async def handle_server_msg(message):
    cmd: str = message.content.replace(INDIC, "")

    if cmd.startswith("running"):
        for i in running():
            poll = getPoll(i)

            send_msg = poll["title"] + "\n" + poll["text"] + "\nDeadline: " + datetime.strftime(poll["deadline"], '%d/%m/%Y %H:%M')

            await message.channel.send(send_msg)
            await send_as_piechart(i, message.channel.id)
            

    #muss raus
    await handle_admin_cmd(message)

    for r in message.author.roles:
        if r.id == 773996048094986241 or r.id == 773993684651212812:
            await handle_admin_cmd(message)

async def handle_admin_cmd(message):
    cmd: str = message.content.replace(INDIC, "")

    if cmd == "help":
        await message.channel.send("Command to create new poll: \n '>new [Option 1, Option 2, usw.] \"Title\" \"Text describing the vote.\" x' where x is the length in hours the poll should run")

    elif cmd.startswith("new"):
        splitted = cmd.split("\"")
        title = splitted[1]
        text = splitted[3]
        hours = splitted[4].strip()
        options = cmd[cmd.find("[")+1 : cmd.find("]")]
        teilnehmer = options.split(",")

        # neue wahl
        createPoll(text, title, "multi", list(map(lambda x: x.strip(), teilnehmer)), int(hours))

    elif cmd.startswith("delete"):
        poll_id = cmd.split(" ")[1]

        # delete call machen

@client.event
async def on_message(message):
    author: Member = message.author

    if author == client.user:
        return

    if not message.content.startswith(INDIC):
        return

    # private channel
    if str(message.channel.type) == "private":
        await handle_private_msg(message)
    # server
    else:
        await handle_server_msg(message)


client.run(TOKEN)