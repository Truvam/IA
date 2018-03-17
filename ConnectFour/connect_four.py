#!/usr/bin/env python3


import copy


player1 = 0
player2 = 1
pc = 3
empty = "_"
width = 7
height = 6


class Board:
    def __init__(self):
        self.board = [["_" for j in range(width)] for i in range(height)]

    def play(self, column, player):
        placed = False
        for i in range(height-1, -1, -1):
            if self.board[i][column] == empty:
                if player == player1 or player == pc:
                    self.board[i][column] = "X"
                else:
                    self.board[i][column] = "O"
                placed = True
                break
        if not placed:
            print("Column %d is full." % column)

    def value_aux(self, cont_x, cont_o):
        if cont_o == 3 and cont_x == 0:
            return -50
        elif cont_o == 2 and cont_x == 0:
            return -10
        elif cont_o == 1 and cont_x == 0:
            return -1
        elif cont_o == 0 and cont_x == 1:
            return 1
        elif cont_o == 0 and cont_x == 2:
            return 10
        elif cont_o == 0 and cont_x == 3:
            return 50
        return 0

    def utility(self):
        cont = 0
        for i in range(0, height):  # DRAW
            for j in range(0, width):
                if self.board[i][j] != empty:
                    cont += 1
                if cont == 42:
                    return 0

        cont_x = 0
        cont_o = 0
        sum = 0
        for i in range(0, height):  # HORIZONTAL
            for j in range(0, width-3):
                for k in range(j, j+4):
                    # print("(%d, %d)" % (i, k))
                    if self.board[i][k] == "X":
                        cont_x += 1
                    elif self.board[i][k] == "O":
                        cont_o += 1      
                if cont_x == 4:
                    return 512
                elif cont_o == 4:
                    return -512
                sum += self.value_aux(cont_x, cont_o)
                cont_x = 0
                cont_o = 0

        for j in range(0, width):  # VERTICAL
            for i in range(0, height-3):
                for k in range(i, i+4):
                    # print("(%d, %d)" % (k, j))
                    if self.board[k][j] == "X":
                        cont_x += 1
                    elif self.board[k][j] == "O":
                        cont_o += 1      
                if cont_x == 4:
                    return 512
                elif cont_o == 4:
                    return -512
                sum += self.value_aux(cont_x, cont_o)
                cont_x = 0
                cont_o = 0

        for i in range(3, height):  # DIAGONAL RIGHT
            z = i
            for j in range(0, width-3):
                for k in range(j, j+4):
                    # print("(%d, %d)" % (z, k))
                    if self.board[z][k] == "X":
                        cont_x += 1
                    elif self.board[z][k] == "O":
                        cont_o += 1
                    z -= 1
                z = i
                if cont_x == 4:
                    return 512
                elif cont_o == 4:
                    return -512
            sum += self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0

        for i in range(3, height):  # DIAGONAL LEFT
            z = i
            for j in range(width-1, width-5, -1):
                for k in range(j, j-4, -1):
                    print("(%d, %d)" % (z, k))
                    if self.board[z][k] == "X":
                        cont_x += 1
                    elif self.board[z][k] == "O":
                        cont_o += 1
                    z -= 1
                z = i
                if cont_x == 4:
                    return 512
                elif cont_o == 4:
                    return -512
            sum += self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0

        self.print_board()
        print("Sum: %d" % sum)
        return sum

    def print_board(self):
        print("  0 1 2 3 4 5 6")
        print(" _______________")
        for i in range(height):
            str = "|"
            for j in range(width):
                str += " " + self.board[i][j]
            print(str + " |")
        print(" ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")


def who_won(result, player):
    if player == player1:
        if result == 0:
            print("Draw!")        
        elif result == 512:
            print("Player1 Won!")
        else:
            print("You Lost!")
    elif player == player2:
        if result == 0:
            print("Draw!")
        elif result == -512:
            print("Player2 Won!")
        else:
            print("Player2 Lost!")
    else:
        if result == 0:
            print("Draw!")        
        elif result == 512:
            print("PC Won!")
        else:
            print("PC Lost!")


def successors(board):
    temp_board = copy.deepcopy(board)
    child_list = list()
    for i in range(0, width):
        # print(i)
        temp_board.play(i, pc)
        child_list.append(temp_board)
        temp_board = copy.deepcopy(board)
    return child_list


def max_value(is_ab, board, alpha, beta):
    print("MAX")
    if board.utility(pc) != -1:
        return board.utility()  # UTILITY(state)
    v = float("-inf")
    for b in successors(board):
        # b.print_board()
        v = max(v, min_value(is_ab, b, alpha, beta))
        if is_ab:
            if v >= beta:
                return v
            alpha = max(alpha, v)
    return v  # needs to be v


def min_value(is_ab, board, alpha, beta):
    print("MIN")
    if board.utility(pc) != -1:
        return board.utility()  # UTILITY(state)
    v = float("inf")
    for b in successors(board):
        # b.print_board()
        v = min(v, max_value(is_ab, b, alpha, beta))
        if is_ab:
            if v <= alpha:
                return v
            beta = min(beta, v)
    return v


def min_max(board):
    v = max_value(False, board, float("-inf"), float("inf"))
    print(v)
    return v


def alpha_beta(board):
    v = max_value(True, board, float("-inf"), float("inf"))
    return v


def player_player(board):
    print("1: Player1")
    print("2: Player2")
    plays_first = input("Who plays first? [1/2]: ")
    p1_turn = True

    if plays_first == "1":
        p1_turn = False

    board.print_board()
    print("Player1 is 'X' and Player2 is 'O'")
    while True:
        if not p1_turn:
            print("Player1 turn.")
            column = int(input("Choose column: "))
            if column == -1:
                print("Ending game...")
                break
            if column > 6 or column < 0:
                print("Column not valid!")
            else:
                board.play(column, player1)
                board.print_board()
                result = board.utility()
                if result in [-512, 512]:
                    who_won(result, player1)
                    break
                p1_turn = True
        else:
            print("Player2 turn.")
            column = int(input("Choose column: "))
            if column == -1:
                print("Ending game...")
                break
            if column > 6 or column < 0:
                print("Column not valid!")
            else:
                board.play(column, player2)
                board.print_board()

                result = board.utility()
                if result in [-512, 512]:
                    who_won(result, player2)
                    break
                p1_turn = False


def player_pc(board):
    print("1: AI - MiniMax")
    print("2: AI - Alpha-Beta")
    ai = input("Option: ")
    plays_first = input("Do you want to play first? [y/n]: ")
    pc_turn = True

    if plays_first == "y" or plays_first == "yes":
        pc_turn = False

    board.print_board()
    print("You are 'O' and PC is 'X'")
    while True:
        if not pc_turn:
            print("Your turn.")
            column = int(input("Choose column: "))
            if column == -1:
                print("Ending game...")
                break
            if column > 6 or column < 0:
                print("Column not valid!")
            else:
                board.play(column, player2)
                board.print_board()

                result = board.utility(player2)
                if result != -1:
                    who_won(result, player2)
                    break
                pc_turn = True
        else:
            print("PC turn.")
            if ai == 1:
                col = min_max(board)
            else:
                col = alpha_beta(board)
            board.play(col, pc)
            board.print_board()
            # result = board.utility(pc)
            # if result != -1:
                # who_won(result, pc)
                # break
            pc_turn = False


def start_game(option):
    board = Board()
    if option == 1:
        player_player(board)
    else:
        player_pc(board)
    # print("DEBUG: Value: %d" % value)


def main():
    print("Connect Four:")
    print("1: Player vs Player")
    print("2: Player vs PC")
    option = int(input("Option: "))
    start_game(option)


if __name__ == '__main__':
    main()
