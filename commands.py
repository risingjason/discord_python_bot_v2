import discord

connect_four_sessions = {}
users_in_c4_session = []

async def cmd_connect_four(client, msg, cmds):
    # correct command looks like this: "!connect4 start @user"
    # @user can any human, if @user is the bot, then play against AI
    # only one player can be in a session at a time
    #if not connect_four_sessions:
    #    if len(cmds) != 3:
    #        await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user`")
    #    elif cmds[0]

    # placing tile command: "!connect4 place X" where X is a column from 1-7


def emoji_board(board):
    # prints connect four game board in emoji form
    pass

commands = { "!connect4":cmd_connect_four }