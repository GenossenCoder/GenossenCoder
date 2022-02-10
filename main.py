from TOKEN import TOKEN
from discord import *
from pie_chart import make_piechart
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from Database import *
import os
from bson import errors

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


async def send_poll(id, channel):  
        poll = getPoll(id)

        send_msg = poll["title"] + "\n" + poll["text"] + "\nDeadline: " + datetime.strftime(poll["deadline"], '%d/%m/%Y %H:%M' + "\n" + "Poll id: "+ str(poll["_id"]))

        await channel.send(send_msg)
        await send_as_piechart(id, channel.id)

@tasks.loop(hours=12)
async def send_chart():
    for i in running():
        await send_poll(i, client.get_channel(940052984904155206))

        
async def handle_private_msg(message):
    cmd: str = message.content.replace(INDIC, "")

    if cmd.startswith("vote"):
        splitted = cmd.split(" ")
        if len(splitted) == 3:
            id = splitted[1]
            vote = splitted[2]
            try:
                poll = getPoll(id)

                for i in poll["competitors"]:
                    if message.author.name in poll[i]:
                        await message.channel.send("You already voted!")
                        return
                
                if vote not in poll["competitors"]:
                    await message.channel.send("Invalid vote choice.")
                    return

                ret = addVote(id, vote, message.author.name)
                if ret == "Success":
                    await message.channel.send("Success!")
                else:
                    await message.channel.send("Datenbank hat nicht geantwortet. Schreib mal Hanns Eisler, der fixt das.")

            except errors.InvalidId:
                await message.channel.send("Invalid poll id.")
            except KeyError:
                await message.channel.send("Invalid vote choice.")
            except:
                await message.channel.send("Unknown error. Schreib mal Hanns Eisler, der fixt das.")

        else:
            await message.channel.send("Vote command must have two parameters.")

async def handle_admin_cmd(message):
    cmd: str = message.content.replace(INDIC, "")

    if cmd == "help":
        await message.channel.send("""
        Commands:
            `>running` Shows all running polls
            `>vote (PollID) (Vote)` Vote for your candidate (!Must be in private channel!)
            `>new [Option 1, Option 2, usw...] "(Title)" "(Text)" (How many hours the poll should run)`
            Bsp: >new [Yes, No] "Whos Coaeyl" "Pls vote wery importand" 72
            `>delete (PollID)`
        """)

    elif cmd.startswith("running"):
        for i in running():
            await send_poll(i, message.channel)

    elif cmd.startswith("new"):
        # hier noch checken ob len richtig ist und sanitizen
        splitted = cmd.split("\"")
        title = splitted[1]
        text = splitted[3]
        hours = splitted[4].strip()
        options = cmd[cmd.find("[")+1 : cmd.find("]")]
        teilnehmer = options.split(",")

        # neue wahl
        createPoll(text, title, "multi", list(map(lambda x: x.strip(), teilnehmer)), int(hours))

    elif cmd.startswith("delete"):
        splitted = cmd.split(" ")

        if len(splitted) == 2:
            try:
                ret = deletePoll(splitted[1])

                if ret == "Success":
                    await message.channel.send("Success!")
                else:
                    await message.channel.send("Datenbank hat nicht geantwortet. Schreib mal Hanns Eisler, der fixt das.")


            except errors.InvalidId:
                await message.channel.send("Invalid poll id.")

        else:
            await message.channel.send("Delete command needs two parameters!")

    # elif cmd.startswith("sos"):
    #     msgs = await message.channel.history(limit=50).flatten()
    #     for i in msgs:
    #         await i.delete()
    #     print("Finished")

async def handle_server_msg(message):
    cmd: str = message.content.replace(INDIC, "")

    #muss raus
    #await handle_admin_cmd(message)

    for r in message.author.roles:
        if r.id == 773996048094986241 or r.id == 773993684651212812:
            await handle_admin_cmd(message)

@client.event
async def on_message(message):
    author: Member = message.author
    cmd: str = message.content.replace(INDIC, "")

    if author == client.user:
        return

    if not message.content.startswith(INDIC):
        return

    # if cmd.startswith("running"):
    #     for i in running():
    #         await send_poll(i, message.channel)

    elif cmd.startswith("help"):
        await message.channel.send("""
        Commands:
            `>vote (PollID) (Vote)` Vote for your candidate (!Must be in private channel!)
        """)

    # private channel
    if str(message.channel.type) == "private":
        await handle_private_msg(message)
    # server
    else:
        await handle_server_msg(message)

client.run(TOKEN)