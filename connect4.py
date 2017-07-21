class ConnectFour:

    def __init__(self):
        self.width = 7
        self.height = 6
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]
        
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
        row = ConnectFour.get_height(self, column)
        self.board[row][column] = player

c = ConnectFour()
c.print_board()
c.insert(3, 1)
c.print_board()