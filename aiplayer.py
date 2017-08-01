from player import *
import sys

class AIPlayer(Player):

    color = None
    player = 0
    opponent = 0
    board = None

    def __init__(self, name, player, board):
        super(Player,self).__init__(name, player, board)

    def move(self, column):
        depth = 5
        current_board = self.board

        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1

        # minimax(current, depth)
        pass
    
    def minimax(self, board, depth):
        legal_moves = []
        best_column = 0
        utility = sys.maxsize * -1
        auxiliary = 0

        # find all legal moves
        for i in range(board.width):
            if board.is_legal(i):
                legal_moves.append(i)
        
        # for moves in legal_moves:
            