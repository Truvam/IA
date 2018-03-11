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
                if player == player1:
                    self.board[i][column] = "X"
                else:
                    self.board[i][column] = "O"
                placed = True
                break
        if not placed:
            print("Column %d is full." % column)
    
    
    def finished(self, player):
        if player == player1:
            play = "X"
        else:
            play = "O"

        cont = 0
        for i in range(0, height):  #DRAW
            for j in range(0, width):
                if self.board[i][j] != empty:
                    cont += 1
                if cont == 42:
                    return 0

        cont = 0
        for i in range(0, height):  #HORIZONTAL
            for j in range(0, width):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 512
            cont = 0

        cont = 0
        for j in range(0, width):  #VERTICAL
            for i in range(0, height):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 512
            cont = 0
        
        cont = 0
        i = 0
        for side in range(3, -1, -1):  #DIAGONAL RIGHT
            for j in range(side, width):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 512
                i += 1
                if(i == 6):
                    break
            cont = 0
            i = 0

        cont = 0
        j = 0
        for side in range(2, -1, -1):  # DIAGONAL LEFT
            for i in range(side, height):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 2
                j += 1
                if (i == 6):
                    break
            cont = 0
            j = 0

        cont = 0
        for i in range(3, 5):  # DIAGONAL UP
            for j in range(0, width):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 512
                i -= 1
                if i < 0:
                    break
            cont = 0

        cont = 0
        i = 5
        for side in range(0, 4):  # DIAGONAL DOWN
            for j in range(side, width):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 512
                i -= 1
                if (i < 0):
                    break
            cont = 0
            i = 5

        return -1
    #dentro da utilidade
    #def utility(self, i, j):

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
        elif result == 512:
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
        print(i)
        temp_board.play(i, pc)
        child_list.append(temp_board)
        temp_board = copy.deepcopy(board)
    return child_list


def max_value(board):
    print("MAX")
    if board.finished(pc) != -1:
        return 0  # UTILITY(state)
    v = float("-inf")
    for b in successors(board):
        b.print_board()
        #v = max(v, min_value(b))
    return 1 #needs to be v


def min_value(board):
    print("MIN")
    if board.finished(pc) != -1:
        return 0  # UTILITY(state)
    v = float("inf")
    for b in successors(board):
        v = min(v, min_value(b))
    return v


def min_max(board):
    v = max_value(board)
    return v


def player_player(board):
    print("1: Player1")
    print("2: Player2")
    plays_first = input("Who plays first? [1/2]: ")
    p1_turn = True

    if plays_first == "1":
        p1_turn = False

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
    plays_first = input("Do you want to play first? [y/n]: ")
    pc_turn = True

    if plays_first == "y" or plays_first == "yes":
        pc_turn = False

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
            v = min_max(board)
            board.play(v, pc)
            board.print_board()
            result = board.finished(pc)
            if result != -1:
                who_won(result, pc)
                break
            pc_turn = False


def start_game(option):
    board = Board()
    board.print_board()
    if option == 1:
        player_player(board)
    else:
        player_pc(board)


def main():
    print("1: Player vs Player")
    print("2: Player vs PC")
    option = int(input("Option: "))
    start_game(option)


if __name__ == '__main__':
    main()
