#!/usr/bin/env python3


import copy


player1 = 0
player2 = 1
pc = 3
empty = "_"
width = 7
height = 6
value = 0


class Board:
    def __init__(self):
        self.board = [["_" for j in range(width)] for i in range(height)]

    def play(self, column, player):
        placed = False
        for i in range(height-1, -1, -1):
            if self.board[i][column] == empty:
                if player == player1:
                    self.board[i][column] = "X"
                else:
                    self.board[i][column] = "O"
                placed = True
                break
        if not placed:
            print("Column %d is full." % column)

    def value_aux(self, cont_x, cont_o):
        global value
        if cont_o == 3 and cont_x == 0:
            value -= 50
        elif cont_o == 2 and cont_x == 0:
            value -= 10
        elif cont_o == 1 and cont_x == 0:
            value -= 1
        elif cont_o == 0 and cont_x == 1:
            value += 1
        elif cont_o == 0 and cont_x == 2:
            value += 10
        elif cont_o == 0 and cont_x == 3:
            value += 50

    def finished(self, player):
        global value
        if player == player1:
            play = "X"
            value += 16
        else:
            play = "O"
            value -= 16

        cont = 0
        cont_x = 0
        cont_o = 0
        for i in range(0, height):  # DRAW
            for j in range(0, width):
                if self.board[i][j] != empty:
                    cont += 1
                if cont == 42:
                    return 0

        cont = 0
        for i in range(0, height):  # HORIZONTAL
            for j in range(0, width):
                if self.board[i][j] == play:
                    if play == "X":
                        cont_x += 1
                    else:
                        cont_o += 1
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    if play == "X":
                        value += 512
                    else:
                        value -= 512
                    return 1
            self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0
            cont = 0

        cont = 0
        for j in range(0, width):  # VERTICAL
            for i in range(0, height):
                if self.board[i][j] == play:
                    if play == "X":
                        cont_x += 1
                    else:
                        cont_o += 1
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    if play == "X":
                        value += 512
                    else:
                        value -= 512
                    return 1
            self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0
            cont = 0
        
        cont = 0
        i = 0
        for side in range(3, -1, -1):  # DIAGONAL RIGHT
            for j in range(side, width):
                if self.board[i][j] == play:
                    if play == "X":
                        cont_x += 1
                    else:
                        cont_o += 1
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    if play == "X":
                        value += 512
                    else:
                        value -= 512
                    return 1
                i += 1
                if(i == 6):
                    break
            self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0
            cont = 0
            i = 0

        cont = 0
        j = 0
        for side in range(2, -1, -1):  # DIAGONAL LEFT
            for i in range(side, height):
                if self.board[i][j] == play:
                    if play == "X":
                        cont_x += 1
                    else:
                        cont_o += 1
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    if play == "X":
                        value += 512
                    else:
                        value -= 512
                    return 1
                j += 1
                if (i == 6):
                    break
            self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0
            cont = 0
            j = 0

        cont = 0
        for i in range(3, 5):  # DIAGONAL UP
            for j in range(0, width):
                if self.board[i][j] == play:
                    if play == "X":
                        cont_x += 1
                    else:
                        cont_o += 1
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    if play == "X":
                        value += 512
                    else:
                        value -= 512
                    return 1
                i -= 1
                if i < 0:
                    break
            self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0
            cont = 0

        cont = 0
        i = 5
        for side in range(0, 4):  # DIAGONAL DOWN
            for j in range(side, width):
                if self.board[i][j] == play:
                    if play == "X":
                        cont_x += 1
                    else:
                        cont_o += 1
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    if play == "X":
                        value += 512
                    else:
                        value -= 512
                    return 1
                i -= 1
                if (i < 0):
                    break
            self.value_aux(cont_x, cont_o)
            cont_x = 0
            cont_o = 0
            cont = 0
            i = 5

        print(value)
        return -1

    def utility(self):
        return value

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
        elif result == 1:
            print("Player1 Won!")
        else:
            print("You Lost!")
    elif player == player2:
        if result == 0:
            print("Draw!")
        elif result == 1:
            print("Player2 Won!")
        else:
            print("Player2 Lost!")
    else:
        if result == 0:
            print("Draw!")        
        elif result == 1:
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
    if board.finished(pc) != -1:
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
    if board.finished(pc) != -1:
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

                result = board.finished(player1)
                if result != -1:
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

                result = board.finished(player2)
                if result != -1:
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
    print("You are 'X' and PC is 'O'")
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
                board.play(column, player1)
                board.print_board()

                result = board.finished(player1)
                if result != -1:
                    who_won(result, player1)
                    break
                pc_turn = True
        else:
            print("PC turn.")
            if ai == 1:
                v = min_max(board)
            else:
                v = alpha_beta(board)
            board.play(v, pc)
            board.print_board()
            # result = board.finished(pc)
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
    print("DEBUG: Value: %d" % value)


def main():
    print("Connect Four:")
    print("1: Player vs Player")
    print("2: Player vs PC")
    option = int(input("Option: "))
    start_game(option)


if __name__ == '__main__':
    main()
