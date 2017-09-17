from c4 import *

class Player(object):
    
    player = 0      # 1 for going first, 2 for going second
    game_board = None

    def __init__(self, name, player, game_board):
        self.name = name
        self.player = player
        self.game_board = game_board
    
    def move(self, column):
        next_move = column

        # error checking will be done by the bot, instead of the Player class
        if self.game_board.insert(next_move, self.player):
            print("{} placed in column {}.".format(self.name, next_move))