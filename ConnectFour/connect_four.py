#!/usr/bin/env python3


import copy


player1 = 0
player2 = 1
pc = 3
empty = "_"
width = 7
height = 6
max_depth = 0


class Board:
    def __init__(self):
        self.board = [["_" for j in range(width)] for i in range(height)]
        self.column = 0
        self.value = 0

    def play(self, column, player):
        placed = False
        for i in range(height-1, -1, -1):
            if self.board[i][column] == empty:
                if player == player1 or player == pc:
                    self.board[i][column] = "X"
                else:
                    self.board[i][column] = "O"
                placed = True
                return placed
        if not placed:
            placed = False
            return placed

    def is_draw(self):
        cont = 0
        for i in range(0, height):  # DRAW
            for j in range(0, width):
                if self.board[i][j] != empty:
                    cont += 1
                if cont == 42:
                    return True
        return False

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
        if self.is_draw():
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

        # print("Sum: %d" % sum)
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


def successors(board, player):
    temp_board = copy.deepcopy(board)
    child_list = list()
    for i in range(0, width):
        if player == pc:
            temp_board.play(i, pc)
        else:
            temp_board.play(i, player2)
        # temp_board.print_board()
        temp_board.column = i
        # temp_board.value = temp_board.utility()
        child_list.append(temp_board)
        temp_board = copy.deepcopy(board)  # nao guardar em memoria
    return child_list


def min_max(board, depth, max_player):
    global max_depth
    move = 0
    v = 0
    v = board.utility()
    if depth == 0 or v in [-512, 512] or board.is_draw():
        board.value = v
        return board
    if max_player:
        best_value = float("-inf")
        for b in successors(board, pc):
            v = min_max(b, depth-1, False).value
            best_value = max(best_value, v)
            if best_value == v:
                move = b.column
        board.value = v
        if depth == max_depth:
            board.column = move
        return board
    else:
        best_value = float("+inf")
        for b in successors(board, player2):
            v = min_max(b, depth-1, True).value
            best_value = min(best_value, v)
            if best_value == v:
                move = b.column
        board.value = v
        if depth == max_depth:
            board.column = move
        return board


def alpha_beta(board, depth, alpha, beta, max_player):
    global max_depth
    move = 0
    v = 0
    value = board.utility()
    if depth == 0 or value in [-512, 512] or board.is_draw():
        board.value = value
        return board
    if max_player:
        best_value = float("-inf")
        for b in successors(board, pc):
            if beta <= alpha:
                break
            v = alpha_beta(b, depth - 1, alpha, beta, False).value
            best_value = max(best_value, v)
            if best_value == v:
                # if v >= beta:
                    # board.value = v
                    # return board
                move = b.column
                alpha = max(alpha, v)
            
        board.value = v
        board.column = move
        return board
    else:
        best_value = float("+inf")
        for b in successors(board, player2):
            if beta <= alpha:
                break
            v = alpha_beta(b, depth - 1, alpha, beta, True).value
            best_value = min(best_value, v)
            if best_value == v:
                # if v <= alpha:
                    # board.value = v
                    # return board
                move = b.column
                beta = min(beta, v)
            
        board.value = v
        board.column = move
        return board


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
            column = input("Choose column: ")
            if column == "":
                print("You forgot to enter the column!")
            else:
                column = int(column)
                if column == -1:
                    print("Ending game...")
                    break
                if column > 6 or column < 0:
                    print("Column not valid!")
                else:
                    if board.play(column, player1):
                        board.print_board()
                        if board.is_draw():
                            who_won(0, player1)
                            break
                        result = board.utility()
                        if result in [-512, 512]:
                            who_won(result, player1)
                            break
                        p1_turn = True
                    else:
                        print("Column is full!")
        else:
            print("Player2 turn.")
            column = input("Choose column: ")
            if column == "":
                print("You forgot to enter the column!")
            else:
                column = int(column)
                if column == -1:
                    print("Ending game...")
                    break
                if column > 6 or column < 0:
                    print("Column not valid!")
                else:
                    if board.play(column, player2):
                        board.print_board()
                        if board.is_draw():
                            who_won(0, player2)
                            break
                        result = board.utility()
                        if result in [-512, 512]:
                            who_won(result, player2)
                            break
                        p1_turn = False
                    else:
                        print("Column is full!")


def player_pc(board):
    global max_depth
    print("1: AI - MiniMax")
    print("2: AI - Alpha-Beta")
    ai = input("Option: ")
    print("Difficulty:")
    print("Depth: 4 (Easy)  Depth: 6 (Medium)  Depth: 8 (Hard)")
    depth = int(input("Depth: "))
    max_depth = depth
    plays_first = input("Do you want to play first? [y/n]: ")
    pc_turn = True

    if plays_first == "y" or plays_first == "yes":
        pc_turn = False

    board.print_board()
    print("You are 'O' and PC is 'X'")
    while True:
        if not pc_turn:
            print("Your turn.")
            column = input("Choose column: ")
            if column == "":
                print("You forgot to enter the column!")
            else:
                column = int(column)
                if column == -1:
                    print("Ending game...")
                    break
                if column > 6 or column < 0:
                    print("Column not valid!")
                else:
                    if board.play(column, player2):
                        board.print_board()
                        if board.is_draw():
                            who_won(0, player2)
                            break
                        result = board.utility()
                        if result in [-512, 512]:
                            who_won(result, player2)
                            break
                        pc_turn = True
                    else:
                        print("Column is full!")
        else:
            print("PC turn.")
            if ai == "1":
                b = min_max(board, depth, True)
            else:
                b = alpha_beta(board, depth, float("-inf"), float("+inf"),
                               True)
            # print("Col: %d" % board.column)
            if board.play(b.column, pc):
                board.print_board()
                if board.is_draw():
                    who_won(0, pc)
                    break
                result = board.utility()
                if result in [-512, 512]:
                    who_won(result, pc)
                    break
                pc_turn = False
            else:
                print("Column is full!")


def start_game(option):
    board = Board()
    if option == 1:
        player_player(board)
    else:
        player_pc(board)
        

def main():
    print("Connect Four:")
    print("1: Player vs Player")
    print("2: Player vs PC")
    option = int(input("Option: "))
    start_game(option)


if __name__ == '__main__':
    main()
