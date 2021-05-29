# create a class to represent the field or board
import random
import time


class MineField():
    def __init__(self, dim_size=10, num_bombs=10):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.dug = set()
        self.create_board()

    def create_board(self):
        self.board = [[None for _ in range(self.dim_size)]
                      for _ in range(self.dim_size)]
        random_squares = random.choices(
            range(self.dim_size ** 2), k=self.num_bombs)
        for rand in random_squares:
            row = rand // self.dim_size
            col = rand % self.dim_size
            self.board[row][col] = '*'

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c]:
                    continue
                self.board[r][c] = self.calculate_num_neighbour_bombs(r, c)

    def calculate_num_neighbour_bombs(self, row, col):
        num = 0
        for r in range(max(0, row - 1), min(self.dim_size, row + 2)):
            for c in range(max(0, col - 1), min(self.dim_size, col + 2)):
                if self.board[r][c] == '*':
                    num += 1

        return num

    def dig(self, row, col):
        time.sleep(0.05)

        # if you stepped on bomb game over
        if self.board[row][col] == '*':
            return False

        self.dug.add((row, col))

        if self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size, row + 2)):
            for c in range(max(0, col - 1), min(self.dim_size, col + 2)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __repr__(self):
        return self.board

    def __str__(self):
        return self.__repr__()

    def show_board(self):
        board = list(self.board)

        # if square is dug show the value otherwise print space

        # print("   || 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ")
        print("   |", end="")
        for c in range(self.dim_size):
            print(f"| {c} ", end="")

        print("\n----", end="")
        print("----" * self.dim_size, end="")
        for r in range(self.dim_size):
            print(f"\n {r} |", end="")
            for c in range(self.dim_size):
                if (r, c) in self.dug:
                    print(f"| {self.board[r][c]} ", end="")
                else:
                    print("|   ", end="")

        print()


def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = MineField(dim_size, num_bombs)

    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
    #          next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        board.show_board()
        # 0,0 or 0, 0 or 0,    0
        user_input = input(
            "\nWhere would you like to dig? Input as row,col: ")  # '0, 3'
        user_input = user_input.split(',')
        user_input = [x.strip() for x in user_input]
        row, col = int(user_input[0]), int(user_input[1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("\nInvalid location. Try again.")
            continue
        if (row, col) in board.dug:
            print("\ncoordinate already dug. Choose another coordinate")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb
            break  # (game over rip)

    if safe:
        print("\nCONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("\nSORRY GAME OVER :(")
        # let's reveal the whole board!
    board.dug = [(r, c) for c in range(board.dim_size)
                 for r in range(board.dim_size)]
    board.show_board()


if __name__ == '__main__':  # only executes the following code when it is run from this module
    play(10, 20)
