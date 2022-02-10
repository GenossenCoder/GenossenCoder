from TOKEN import TOKEN
from discord import *
from pie_chart import make_piechart
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from Database import *

INDIC = ">"
client = Client()


async def send_as_piechart(id):            
    dic: dict = get_status(id)
    make_piechart(list(dic.keys()), list(dic.values()))

    with open("pie.png", "rb") as f:
        f = discord.File(f)
        await client.get_channel(940052984904155206).send(file=f)
    

@tasks.loop(hours=12)
async def send_chart():
    if running() == None:
       return
    else:
        for i in running():
            send_as_piechart(i)
        
async def handle_private_msg(message):
    cmd: str = message.content.replace(INDIC, "")

    if cmd.startswith("show"):
        x = 0
        for i in running():
            x += 1
            send_as_piechart(i)
            await message.channel.send(getPoll(i))

            # hier nachricht vom user awaiten und dann add_vote aufrufen

async def handle_server_msg(message):
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
        name = splitted[1]
        text = splitted[2]
        hours = splitted[3].strip()
        options = cmd[cmd.find("[")+1 : cmd.find("]")]
        teilnehmer = options.split(",")
        print(list(map(lambda x: x.strip(), teilnehmer)))
        # neue wahl
        createPoll(text, title, "multi", list(map(lambda x: x.trim(), teilnehmer)), hours)

    #running muss in nicht admin funktion
    elif cmd.startswith("running"):
        # print laufenden wahlen
        pass

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