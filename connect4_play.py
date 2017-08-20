import discord
from connect4 import *
from player import *

connect_four_sessions = {}
users_in_c4_session = {}

connect_four_syntax = "```Connect4! Start game with !connect4 start @user\n" +\
                      "- start: the person who types the message is player 1 and @user is player 2\n" +\
                      "- play: !c4 p (column) to place a piece in a column from 1-7\n" +\
                      "- if @user is this bot, then you will play against an AI (currently in development)```"

async def connect_four(client, msg, cmds):
    # correct command looks like this: "!connect4 start @user" ex. user mention string <@153142506014507008>
    # @user can any human, if @user is the bot, then play against AI
    # only one player can be in a session at a time
    mentions = msg.mentions
    first_user_id = msg.author.id
    
    # display connect4 syntax
    if len(cmds) == 1:
        await client.send_message(msg.channel, connect_four_syntax)
        return

    # case: !connect4 asdf asf asdf
    if len(cmds) != 3:
        await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user OR !connect4 place (column)`")
        return

    # case: !connect4 asdfsaf
    if cmds[1] != "start" and cmds[1] != "p" and cmds[1] != "stop":
        await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user OR !connect4 place (column)`")
        return
    
    
    # case: !connect4 start @user_in_session
    if cmds[1] == "start":
        # case: !connect4 start @non_existent_user
        if not mentions:
            await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user`")
            return
        # case: !connect4 start @user1 @user2 ...
        if len(mentions) > 1:
            await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 start @user`")

        second_user_id = mentions[0].id
        await start_game(client, msg, cmds, mentions, first_user_id, second_user_id)
        return

    # placing tile command: "!connect4 place X" where X is a column from 1-7
    if cmds[1] == "p":
        await place_piece(client, msg, cmds, first_user_id)
        return

    # force quit game session command
    if cmds[1] == "stop":
        if cmds[2] != "game":
            await client.send_message(msg.channel, "`Invalid Command Example command: !connect4 stop game`")
            return
        else:
            opponent = await force_stop(client, msg, first_user_id)
            await client.send_message(msg.channel, "{}` has force quit their connect four game against `{}`.`".format(msg.author.mention, "<@" + opponent + ">"))
            return

async def start_game(client, msg, cmds, mentions, first_user_id, second_user_id):
    # case: message author is already in game session
    if first_user_id in users_in_c4_session:
        await client.send_message(msg.channel, "{}` is in another Connect4 session. Only one session is allowed per user.`".format(str(msg.author.mention)))
        return
    # case: opponent is already in game session
    elif second_user_id in users_in_c4_session.values():
        await client.send_message(msg.channel, "{}` is in another Connect4 session. Only one session is allowed per user.`".format(str(mentions[0].mention)))
        return
    # case: person is trying to play against themselves
    elif first_user_id == second_user_id:
        await client.send_message(msg.channel, "`You cannot play against yourself! Play against another human or AI.`")
        return
    else:
        await client.send_message(msg.channel, "{}`is now playing against `{}".format("<@" + first_user_id + ">", "<@" + second_user_id + ">"))
        create_game(first_user_id, second_user_id)
        emoji = emoji_board(connect_four_sessions[first_user_id])
        await client.send_message(msg.channel, emoji + "\n{} vs. {}".format("<@" + first_user_id + ">", "<@" + second_user_id + ">"))
    return

async def place_piece(client, msg, cmds, first_user_id):
    # case: user did not put a column number on command, otherwise save the number
    column_number = None
    try:
        column_number = int(cmds[2])
    except:
        pass

    # case: user put an incorrect column number
    if isinstance(column_number, int):
        if column_number > 7 or column_number < 1:
            await client.send_message(msg.channel, "`Please choose a column number from 1-7.`")
            return
    else:
        await client.send_message(msg.channel, "`Invalid Command. Example command: !connect4 place (column) where column is 1-7`")
        return

    # case: message author is not in a session
    if not first_user_id in users_in_c4_session and not first_user_id in users_in_c4_session.values():
        await client.send_message(msg.channel, "{}` is not in a Connect4 session. You must start a session before being able to place on the board.`".format(str(msg.author.mention)))
        return
    else:
        await make_move(client, msg, cmds, first_user_id, column_number)
        return

async def make_move(client, msg, cmds, first_user_id, column):
    player_flag = 0
    invert_users = {value: key for key, value in users_in_c4_session.items()}
    try:
        player_flag = 2
        who_is = invert_users[first_user_id] # gets player1 of the board to grab the board from the dictionary
        second_user_id = first_user_id  # this is because the message author is player 2
    except:
        player_flag = 1
        who_is = first_user_id
        second_user_id = users_in_c4_session[first_user_id]

    print("Successful Place Command")
    current_board = connect_four_sessions[who_is]
    if player_flag == 1 and current_board.turn == 1:
        current_board.player1.move(column-1)
    elif player_flag == 2 and current_board.turn == 2:
        current_board.player2.move(column-1)
    else:
        await client.send_message(msg.channel, "`It is currently not your turn. Please wait until your opponent makes a move.`")
        return

    emojis = emoji_board(current_board)
    await client.send_message(msg.channel, emojis + "\n{} vs. {}".format("<@" + who_is + ">", "<@" + second_user_id + ">"))
    await check_winner(client, msg, cmds, who_is, current_board)
    return

async def check_winner(client, msg, cmds, first_user_id, board): 
    # if game ended, print winner, otherwise print game draw
    if board.game_end:
        print("Hello Game Win")
        if board.game_draw:
            print("hello Game Draw")
            await client.send_message(msg.channel, "`This game is a draw!`")
        else:
            await client.send_message(msg.channel, "`The winner is `{}`!`".format(msg.author.mention))
            
        del connect_four_sessions[first_user_id]
        del users_in_c4_session[first_user_id]

    return

async def force_stop(client, msg, user):
    player_flag = 0
    invert_users = {value: key for key, value in users_in_c4_session.items()}
    if not user in users_in_c4_session and not user in users_in_c4_session.values():
        await client.send_message(msg.channel, "`You are currently not in a session. Start a new session with !connect4 start @user`")
        return

    try:
        player_flag = 2
        who_is = invert_users[user] # gets player1 of the board to grab the board from the dictionary
        second_user_id = who_is # in this case, you want the opponent of user to be second_user
    except:
        player_flag = 1
        who_is = user
        second_user_id = users_in_c4_session[user]
    
    del connect_four_sessions[who_is]
    del users_in_c4_session[who_is]
    return second_user_id

def create_game(first_user_id, second_user_id):
    print("Successful Start Command")

    # create board and players
    connect_four_game = ConnectFour()
    play1 = Player(first_user_id, 1, connect_four_game)
    play2 = Player(second_user_id, 2, connect_four_game)
    connect_four_game.set_player(play1, 1)
    connect_four_game.set_player(play2, 2)

    # add board to dictionary
    users_in_c4_session[first_user_id] = second_user_id
    connect_four_sessions[first_user_id] = connect_four_game
    print("Connect 4 Key is on {}".format(first_user_id))
    print("p1: {}, p2: {}".format(users_in_c4_session[first_user_id], second_user_id))


def emoji_board(connect4_obj):
    # prints connect four game board in emoji form
    player_one_circle = ":red_circle:"
    player_two_circle = ":large_blue_circle:"
    empty_space = ":white_circle:"
    emoji_board = ""
    emoji_nums = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:"]

    for row in reversed(range(connect4_obj.height)):
        for col in range(connect4_obj.width):
            if connect4_obj.board[row][col] == 1:
                emoji_board += player_one_circle + " "
            elif connect4_obj.board[row][col] == 2:
                emoji_board += player_two_circle + " "
            elif connect4_obj.board[row][col] == 0:
                emoji_board += empty_space + " "
        emoji_board += "\n"

    emoji_board += " ".join(emoji_nums)        
    return emoji_board