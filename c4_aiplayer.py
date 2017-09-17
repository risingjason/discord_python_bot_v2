from c4_player import *
from c4 import *
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
        print("player: {}".format(player))

    def get_ai_move(self):
        depth = 5
        current_game_state = ConnectFour()
        current_game_state.board = copy.deepcopy(self.game_board.board)

        next_move = self.minimax(current_game_state, depth)
        self.move(next_move)

    def minimax(self, game_state, depth):
        legal_moves = []
        best_column = 0
        score = -999999999
        trial = None

        # find all legal moves
        for col in range(game_state.width):
            if game_state.is_legal(col):
                legal_moves.append(col)
        
        for moves in legal_moves:
            game_state.insert(moves, self.player)

            trial = self.min_value(game_state, depth-1)# + self.middle_bias(game_state, moves)
            print("score: {} move: {}".format(trial, moves))
            
            # better move found, update score
            if trial >= score:
                best_column = moves
                score = trial
            
            game_state.undo_move()
        
        return best_column

    def min_value(self, game_state, depth):
        legal_moves = []
        minimum = 999999999
        min_trial = None

        if depth <= 0 or game_state.game_end:
            return self.evaluation(game_state, self.opponent)

        for col in range(game_state.width):
            if game_state.is_legal(col):
                legal_moves.append(col)
        
        for moves in legal_moves:
            game_state.insert(moves, self.opponent)

            min_trial = self.max_value(game_state, depth-1)
            
            if min_trial <= minimum:
                minimum = min_trial
            
            game_state.undo_move()
        
        return minimum

    def max_value(self, game_state, depth):
        legal_moves = []
        maximum = -999999999
        max_trial = None

        if depth <= 0 or game_state.game_end:
            return self.evaluation(game_state, self.player)

        for col in range(game_state.width):
            if game_state.is_legal(col):
                legal_moves.append(col)
        
        for moves in legal_moves:
            game_state.insert(moves, self.player)

            max_trial = self.min_value(game_state, depth-1)

            if max_trial >= maximum:
                maximum = max_trial
            
            game_state.undo_move()
        
        return maximum

    def middle_bias(self, game_state, column):
        width_bias = [2, 4, 5, 7, 5, 4, 2]
        height_bias = [2, 2, 3, 3, 2, 1]
        index = game_state.get_height(column)

        return (height_bias[index] + width_bias[column])

    def evaluation(self, game_state, player):
        result = 0

        if not game_state.game_end:
            # pass
            result = self.heuristic(game_state, player)
        else:
            if game_state.winning_player == self.player:
                result = 10000
            elif game_state.winning_player == self.opponent:
                result = -10000

        return result

    def heuristic(self, game_state, player):
        result = 0
        board = game_state.board
        last_col = game_state.last_moves[-1]
        last_hei = game_state.get_height(last_col) - 1

        # check -
        if last_col < 6:
            if board[last_hei][last_col] == board[last_hei][last_col+1] == player:
                print("comes here")
                if board[last_hei][last_col+2] == player:
                    print("Comes here too")
                    result += 10
                else:
                    result += 5

        return result