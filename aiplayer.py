from player import *
from connect4 import *
import copy
import sys

class AIPlayer(Player):

    player = 0
    opponent = 0
    game_board = None

    def __init__(self, name, player, game_board):
        super().__init__(name, player, game_board)
        if player == 1:
            self.opponent = 2
        elif player == 2:
            self.opponent = 1

    def get_ai_move(self):
        depth = 4
        #current_game_state = copy.copy(self.game_board)
        current_game_state = ConnectFour()
        current_game_state.board = copy.deepcopy(self.game_board.board)

        next_move = self.minimax(current_game_state, depth)
        self.move(next_move)

    def minimax(self, game_state, depth):
        legal_moves = []
        best_column = 0
        score = sys.maxsize * -1
        trial = None

        # find all legal moves
        for col in range(game_state.width):
            if game_state.is_legal(col):
                legal_moves.append(col)
        
        # for moves in legal_moves:
        for moves in legal_moves:
            game_state.insert(moves, self.player)
            #game_state.print_board()
            #self.move(moves)
            trial = self.min_value(game_state, depth-1) + self.middle_bias(game_state, moves)
            print("score: {} move: {}".format(trial, moves))
            # better move found, update score
            if trial >= score:
                best_column = moves
                score = trial
            
            game_state.undo_move(moves)
        
        return best_column

    def min_value(self, game_state, depth):
        legal_moves = []
        minimum = sys.maxsize
        min_trial = None

        if depth <= 0 or game_state.game_end:
            # print("depth: {}".format(depth))
            return self.evaluation(game_state, self.opponent)

        for col in range(game_state.width):
            if game_state.is_legal(col):
                legal_moves.append(col)
        
        for moves in legal_moves:
            # print("Opponent is {}".format(self.opponent))
            game_state.insert(moves, self.opponent)
            #game_state.print_board()
            min_trial = self.max_value(game_state, depth-1)

            if min_trial <= minimum:
                minimum = min_trial

            game_state.undo_move(moves)
        
        return minimum

    def max_value(self, game_state, depth):
        legal_moves = []
        maximum = sys.maxsize * -1
        max_trial = None

        if depth <= 0 or game_state.game_end:
            # print("depth: {}".format(depth))
            return self.evaluation(game_state, self.player)

        for col in range(game_state.width):
            if game_state.is_legal(col):
                legal_moves.append(col)
        
        for moves in legal_moves:
            game_state.insert(moves, self.player)
            #game_state.print_board()
            #self.move(moves)
            max_trial = self.min_value(game_state, depth-1)

            if max_trial >= maximum:
                maximum = max_trial
            
            game_state.undo_move(moves)
        
        return maximum

    def middle_bias(self, game_state, column):
        width_bias = [1, 2, 3, 4, 3, 2, 1]
        height_bias = [2, 3, 4, 4, 2, 1]
        index = game_state.get_height(column)

        value = abs(4 - index - 1)
        return (height_bias[index] + width_bias[column])

    def evaluation(self, game_state, player):
        result = 0

        if not game_state.game_end:
            result = self.heuristic(game_state, player)
        else:
            if game_state.winning_player == self.player:
                result = 100000
            elif game_state.winning_player == self.opponent:
                # print("comes here")
                result = -100000

        #print("score: {}".format(result))
        return result

    def heuristic(self, game_state, player):
        result = 0

        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1

        for row in range(game_state.height):
            for col in range(game_state.width):
                #result += self.get_four(game_state, player, row, col)
                result += abs(self.get_three(game_state, player, opponent, row, col))
                result += abs(self.get_two(game_state, player, opponent, row, col))
                # result -= self.get_three(game_state, opponent, row, col)
                # result -= self.get_two(game_state, opponent, row, col)

        return result

    def get_four(self, game_state, player, row, col):
        score = 0
        
        # check horizontal
        if col < 4:
            if game_state.board[row][col] == game_state.board[row][col+1] == game_state.board[row][col+2] == game_state.board[row][col+3] == player:
                score += 100000

        # check vertical
        if row < 3:
            if game_state.board[row][col] == game_state.board[row+1][col] == game_state.board[row+2][col] == game_state.board[row+3][col] == player:
                score += 100000
        
        # check diagonal
        if row < 3 and col < 4:
            if game_state.board[row][col] == game_state.board[row+1][col+1] == game_state.board[row+2][col+2] == game_state.board[row+3][col+3] == player:
                score += 100000
        
        # check diagonal
        if row < 3 and col > 2:
            if game_state.board[row][col] == game_state.board[row+1][col-1] == game_state.board[row+2][col-2] == game_state.board[row+3][col-3] == player:
                score += 100000
        
        return score

    def get_three(self, game_state, player, opponent, row, col):
        score = 0
        
        # check horizontal
        if col < 5:
            if game_state.board[row][col] == game_state.board[row][col+1] == game_state.board[row][col+2] == player:
                score += 100
            elif game_state.board[row][col] == game_state.board[row][col+1] == game_state.board[row][col+2] == opponent:
                score -= 50
        
        # check vertical
        if row < 4:
            if game_state.board[row][col] == game_state.board[row+1][col] == game_state.board[row+2][col] == player:
                score += 100
            elif game_state.board[row][col] == game_state.board[row+1][col] == game_state.board[row+2][col] == opponent:
                score -= 50
        
        
        # check diagonal
        if row < 4 and col < 5:
            if game_state.board[row][col] == game_state.board[row+1][col+1] == game_state.board[row+2][col+2] == player:
                score += 100
            elif game_state.board[row][col] == game_state.board[row+1][col+1] == game_state.board[row+2][col+2] == opponent:
                score -= 50
        
        
        # check diagonal
        if row < 4 and col > 1:
            if game_state.board[row][col] == game_state.board[row+1][col-1] == game_state.board[row+2][col-2] == player:
                score += 100
            elif game_state.board[row][col] == game_state.board[row+1][col-1] == game_state.board[row+2][col-2] == opponent:
                score -= 50
        
        
        return score

    def get_two(self, game_state, player, opponent, row, col):
        score = 0
        
        # check horizontal
        if col < 6:
            if game_state.board[row][col] == game_state.board[row][col+1] == player:
                score += 10
            elif game_state.board[row][col] == game_state.board[row][col+1] == opponent:
                score -= 5
        
        # check vertical
        if row < 5:
            if game_state.board[row][col] == game_state.board[row+1][col] == player:
                score += 10
            elif game_state.board[row][col] == game_state.board[row+1][col] == opponent:
                score -= 5
        
        # check diagonal
        if row < 5 and col < 6:
            if game_state.board[row][col] == game_state.board[row+1][col+1] == player:
                score += 10
            elif game_state.board[row][col] == game_state.board[row+1][col+1] == opponent:
                score -= 5
        
        # check diagonal
        if row < 5 and col != 0:
            if game_state.board[row][col] == game_state.board[row+1][col-1] == player:
                score += 10
            elif game_state.board[row][col] == game_state.board[row+1][col-1] == opponent:
                score -= 5
        
        return score

