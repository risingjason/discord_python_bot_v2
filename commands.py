import discord
from connect4 import *
from player import *

connect_four_sessions = {}
users_in_c4_session = {}

connect_four_syntax = "`Connect4! Start game with !connect4 start @user" +\
                      "- start: the person who types the message is player 1 and @user is player 2" +\
                      "- play: !connect4 place (column) to place a piece in a column from 1-7" +\
                      "- if @user is this bot, then you will play against an AI (currently in development)`"

async def cmd_connect_four(client, msg, cmds):
    # correct command looks like this: "!connect4 start @user" ex. user mention string <@153142506014507008>
    # @user can any human, if @user is the bot, then play against AI
    # only one player can be in a session at a time
    # print(cmds[2][2:-1])

    # display connect4 syntax
    if len(cmds) == 1:
        await client.send_message(msg.channel, connect_four_syntax)
        return

    # case: !connect4 asdf asf asdf
    if len(cmds) != 3:
        await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user`")
        return

    # case: !connect4 asdfsaf
    if cmds[1] != "start":
        await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user`")
        return

    # case: !connect4 start @user_in_session
    if cmds[1] == "start" and cmds[2][2:-1] in users_in_c4_session:
        await client.send_message(msg.channel, "`This user is in another Connect4 session. Only one session is allowed per user.`")
        return
    else:
        connect_four_game = ConnectFour()
        play1 = Player(msg.author.id, 1, connect_four_game)
        play2 = Player(cmds[2][2:-1], 2, connect_four_game)
        connect_four_game.set_player(play1, 1)
        connect_four_game.set_player(play2, 2)
        emojis = emoji_board(connect_four_game)
        await client.send_message(msg.channel, emojis)
        


    # placing tile command: "!connect4 place X" where X is a column from 1-7

def emoji_board(connect4_obj):
    # prints connect four game board in emoji form
    player_one_circle = ":red_circle:"
    player_two_circle = ":large_blue_circle:"
    empty_space = ":white_circle:"
    emoji_board = ""
    emoji_nums = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:"]
    for row in reversed(range(connect4_obj.height)):
        #print("Row: " + str(row), end=" ")
        # emoji_board += emoji_nums[row]     #printing the rows looks ugly

        for col in range(connect4_obj.width):
            #print(connect4_obj.board[row][col], end=" ")
            if connect4_obj.board[row][col] == 1:
                emoji_board += player_one_circle + " "
            elif connect4_obj.board[row][col] == 2:
                emoji_board += player_two_circle + " "
            elif connect4_obj.board[row][col] == 0:
                emoji_board += empty_space + " "
        emoji_board += "\n"

    emoji_board += " ".join(emoji_nums)        
    return emoji_board

commands = { "!connect4":cmd_connect_four }

