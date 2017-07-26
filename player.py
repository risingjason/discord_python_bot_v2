
class Player(object):
    
    color = None
    player = 0      # 1 for going first, 2 for going second
    board = None

    def __init__(self, name, player, board):
        self.name = name
        self.player = player
        if player == 1:
            self.color = "red"
        elif player == 2:
            self.color = "blue"
        self.board = board
    
    def move(self, column):
        next_move = column

        # error checking will be done by the bot, instead of the Player class
        if self.board.insert(next_move, self.player):
            print("{0} piece placed in column {1}.".format(self.color, next_move))  