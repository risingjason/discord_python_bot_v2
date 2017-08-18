from player import *

class ConnectFour(object):
    game_end = False
    game_draw = False
    player1 = None
    player2 = None
    turn = None

    def __init__(self):
        self.width = 7
        self.height = 6
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]
        self.turn = 1
    
    # set the player object
    def set_player(self, player, num):
        if num == 1:
            self.player1 = player
        elif num == 2:
            self.player2 = player
        else:
            return

    # print the 2D array for testing purposes
    def print_board(self):
        for row in reversed(range(self.height)):
            print("Row: " + str(row), end="| ")
            for col in range(self.width):
                print(self.board[row][col], end=" ")
            print()
        print("---------------------")
        print("Col: -| 1 2 3 4 5 6 7")

    # returns the height where the next piece would be placed
    # returns -1 if the column is filled
    def get_height(self, column):
        for row in range(self.height):
            if self.board[row][column] == 0:
                return row
        return -1

    # returns True when works as intended, returns False when it does not
    def insert(self, column, player):
        # cannot insert even though there is no winner
        if self.game_end:
            print("Cannot insert. The game has already been completed.")
            return False

        # illegal move
        if not self.is_legal(column):
            print("Cannot insert. Illegal move.")
            return False

        # change turns
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1

        row = self.get_height(column)
        self.board[row][column] = player

        # find winner, game ends when there is a winner
        if self.is_winner(player):
            self.game_end = True
            # print("Player {} is Winner!".format(player))
        elif self.full_board():
            self.game_end = True
            self.game_draw = True
            # print("Draw!")
        return True

    def undo_move(self, column):
        current_height = self.get_height(column)
        self.board[current_height-1][column] = 0

    def is_legal(self, column):
        if column > 6 or column < 0:
            return False
        if self.get_height(column) == -1:
            return False
        if not isinstance(column, int):
            return False
        return True

    def full_board(self):
        # for row in range(self.height):
        #     for col in range(self.width):
        #         if self.board[row][col] == 0:
        #             return False
        for col in range(self.width):
            if self.get_height(col) != -1:
                return False
        return True

    def is_winner(self, player):
        # check for horizontal -- winner
        for row in range(self.height-3):
            for col in range(self.width):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] == player:
                    return True

        # check for vertical | winner
        for row in range(self.height):
            for col in range(self.width-3):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3] == player:
                    return True

        # check for diagonal / winner
        for row in range(self.height-3):
            for col in range(self.width-3):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] == player:
                    return True
    
        # check for diagonal \ winner
        for row in range(self.height-3):
            for col in range(3,self.width-3):
                if self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3] == player:
                    return True
        
        return False


## TESTING GOES HERE ##
# c = ConnectFour()
# p1 = Player("red", 1, c)
# p2 = Player("blue", 2, c)
# c.set_player(p1, 1)
# c.set_player(p2, 2)
# c.print_board()

## TEST LEGAL MOVES ##
# c.insert(7, 1)

## TEST WINNING ##
# p1.move(3)
# c.print_board()

# p2.move(2)
# p1.move(2)
# c.print_board()

# p2.move(1)
# p2.move(1)
# p1.move(1)
# c.print_board()

# p2.move(0)
# p1.move(0)
# p2.move(0)
# p1.move(0)
# c.print_board()

# p1.move(4)

## TEST DRAW ##
# c.insert(0, 3)
# c.insert(0, 3)
# c.insert(0, 3)
# c.insert(0, 1)
# c.insert(0, 3)
# c.insert(0, 3)


# c.insert(1, 4)
# c.insert(1, 4)
# c.insert(1, 4)
# c.insert(1, 2)
# c.insert(1, 4)
# c.insert(1, 4)


# c.insert(2, 5)
# c.insert(2, 5)
# c.insert(2, 5)
# c.insert(2, 1)
# c.insert(2, 5)
# c.insert(2, 5)


# c.insert(3, 6)
# c.insert(3, 6)
# c.insert(3, 6)
# c.insert(3, 7)
# c.insert(3, 6)
# c.insert(3, 6)


# c.insert(4, 1)
# c.insert(4, 1)
# c.insert(4, 1)
# c.insert(4, 2)
# c.insert(4, 1)
# c.insert(4, 1)

# c.insert(5, 9)
# c.insert(5, 9)
# c.insert(5, 9)
# c.insert(5, 8)
# c.insert(5, 9)
# c.insert(5, 9)


# c.insert(6, 5)
# c.insert(6, 5)
# c.insert(6, 5)
# c.insert(6, 6)
# c.insert(6, 5)
# c.insert(6, 5)

# c.print_board()