import discord
import connect4_play

async def cmd_connect_four(client, msg, cmds):
    await connect4_play.connect_four(client, msg, cmds)
    return

commands = { "!c4":cmd_connect_four, "!connect4":cmd_connect_four }