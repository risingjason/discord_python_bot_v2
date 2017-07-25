from player import *

class ConnectFour(object):
    player1 = None
    player2 = None
    game_end = False

    def __init__(self, player1, player2):
        self.width = 7
        self.height = 6
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]
        self.player1 = Player(player1, 1)
        self.player2 = Player(player2, 2)
        
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

    def insert(self, column, player):
        # cannot insert even though there is no winner
        if self.game_end:
            print("Cannot insert. The game has already been comleted.")
            return

        row = self.get_height(column)
        self.board[row][column] = player
        if self.is_winner(player):
            self.game_end = True
            print("Player {} is Winner!".format(player))
        elif self.full_board():
            self.game_end = True
            print("Draw!")
        return

    def full_board(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 0:
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

p1 = Player("red", 1)
p2 = Player("blue", 1)
c = ConnectFour(p1, p2)
c.print_board()

c.insert(3, 1)
c.print_board()

c.insert(2, 2)
c.insert(2, 1)
c.print_board()

c.insert(1, 2)
c.insert(1, 2)
c.insert(1, 1)
c.print_board()

c.insert(0, 2)
c.insert(0, 1)
c.insert(0, 2)
c.insert(0, 1)
c.print_board()

c.insert(4, 2)