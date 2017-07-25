
class Player(object):
    
    color = None
    player = 0      # 1 for going first, 2 for going second

    def __init__(self, color, player):
        self.color = color
        self.player = player
    
    def move(self, column, board):
        pass