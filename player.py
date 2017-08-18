
class Player(object):
    
    player = 0      # 1 for going first, 2 for going second
    board = None
    color = None

    def __init__(self, name, player, board):
        self.name = name
        self.player = player
        self.board = board
        if player == 1:
            self.color = "red"
        elif player == 2:
            self.color = "blue"
    
    def move(self, column):
        next_move = column

        # error checking will be done by the bot, instead of the Player class
        if self.board.insert(next_move, self.player):
            print("{0} piece placed in column {1}.".format(self.color, next_move))