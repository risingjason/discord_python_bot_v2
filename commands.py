import discord

connect_four_sessions = {}
users_in_c4_session = []

connect_four_rules = "`Connect4! Start game with !connect4 start @user" +\
                     "- start: the person who types the message is player 1 and @user is player 2" +\
                     "- play: !connect4 place (column) to place a piece in a column from 1-7" +\
                     "- if @user is this bot, then you will play against an AI (currently in development)`"

async def cmd_connect_four(client, msg, cmds):
    # correct command looks like this: "!connect4 start @user" ex. user mention string <@153142506014507008>
    # @user can any human, if @user is the bot, then play against AI
    # only one player can be in a session at a time
    #print(cmds[2][2:-1])
    if len(cmds) == 1:
        await client.send_message(msg.channel, connect_four_rules)
        return

    if not connect_four_sessions:
        if len(cmds) != 3:
            await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user`")
        
        if cmds[1] == "start" and cmds[2][2:-1] in users_in_c4_session:
            await client.send_message(msg.channel, "")

    # placing tile command: "!connect4 place X" where X is a column from 1-7

def emoji_board(board):
    # prints connect four game board in emoji form
    pass

commands = { "!connect4":cmd_connect_four }