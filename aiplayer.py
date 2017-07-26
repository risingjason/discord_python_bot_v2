from player import *
class AIPlayer(Player):

    color = None
    player = 0

    def __init__(self, name, player):
        super(Player,self).__init__(name, player, board)

    def move(self, column):
        pass