#!/usr/bin/env python3


import copy
import time
import resource


player1 = 0
player2 = 1
pc = 3
pc2 = 4
empty = "_"
width = 7
height = 6
max_depth = 0
n_nodes = 0


class Board:
    def __init__(self):
        self.board = [["_" for j in range(width)] for i in range(height)]
        self.column = 0
        self.value = 0

    def play(self, column, player):
        """
        This function is used to place the piece, of the chosen column,
        in the board.
        :param column: column where piece enters;
        :param player: the player that places the piece
        :return: returns True or False whether the piece was placed
        successfully.
        """

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
        """
        This counts each piece in the board, to check if it is a draw.
        :return: returns True or False whether the current board state is a
        draw.
        """
        cont = 0
        for i in range(0, height):  # DRAW
            for j in range(0, width):
                if self.board[i][j] != empty:
                    cont += 1
                if cont == 42:
                    return True
        return False

    def value_aux(self, cont_x, cont_o):
        """
        This is the evaluation function, which help the utility in
        order to count the points of a given board.
        :param cont_x: number of "X" in the segment;
        :param cont_o: number of "O" in the segment;
        :return: returns the points.
        """
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
        """
        This is used in conjunction with the value_aux, to verify if the
        current board is win or loss and to return the sum of the evaluation
        points.
        :return: returns 0 if it's draw, 512 if won, -512 if lost and the
        sum of the evaluation function.
        """
        if self.is_draw():
            return 0
        cont_x = 0
        cont_o = 0
        sum = 0
        for i in range(0, height):  # HORIZONTAL
            for j in range(0, width-3):
                for k in range(j, j+4):
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
    elif player == pc:
        if result == 0:
            print("Draw!")        
        elif result == 512:
            print("PC 1 Won!")
        else:
            print("PC 1 Lost!")
    else:
        if result == 0:
            print("Draw!")
        elif result == 512:
            print("PC 2 Won!")
        else:
            print("PC 2 Lost!")


def successors(board, player):
    """
    This creates all the possible moves that a player can make in the current
    board.
    :param board: current board state;
    :param player: current player;
    :return: returns a list of the board successors.
    """
    global n_nodes
    temp_board = copy.deepcopy(board)
    child_list = list()
    for i in range(0, width):
        temp_board.play(i, player)
        temp_board.column = i
        n_nodes += 1
        child_list.append(temp_board)
        temp_board = copy.deepcopy(board)
    return child_list


def min_max(board, depth):
    """
    Minimax algorithm.
    :param board: current board state;
    :param depth: maximum depth;
    :return: returns the column.
    """
    value = float("-inf")
    column = 0
    for s in successors(board, pc):  # maximizer player
        v = min_value(s, depth - 1)
        if v >= value:
            value = v
            column = s.column
    return column
 

def min_value(board, depth):
    """
    Minimizing Player.
    :param board: current board state;
    :param depth: current depth;
    :return: returns the best value.
    """
    value = board.utility()
    if depth == 0 or value in [-512, 512] or board.is_draw():
        return value
    v = float("inf")
    for s in successors(board, player2):
        v = min(v, max_value(s, depth - 1))
    return v
    

def max_value(board, depth):
    """
    Maximizing Player.
    :param board: current board state;
    :param depth: current depth;
    :return: returns the best value.
    """
    value = board.utility()
    if depth == 0 or value in [-512, 512] or board.is_draw():
        return value
    v = float("-inf")
    for s in successors(board, pc):
        v = max(v, min_value(s, depth - 1))
    return v
    

def alpha_beta(board, depth, alpha, beta):
    """
    Alpha-beta algorithm.
    :param board: current board state;
    :param depth: maximum depth;
    :return: returns the column.
    """
    value = float("-inf")
    column = 0
    for s in successors(board, pc):
        v = min_value_ab(s, depth - 1, alpha, beta)
        if v >= value:
            value = v
            column = s.column
            if value >= beta:
                break
    return column
 

def min_value_ab(board, depth, alpha, beta):
    """
    Minimizing Player.
    :param board: current board state;
    :param depth: current depth;
    :return: returns the best value.
    """
    value = board.utility()
    if depth == 0 or value in [-512, 512] or board.is_draw():
        return value
    v = float("inf")
    for s in successors(board, player2):
        v = min(v, max_value_ab(s, depth - 1, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
    

def max_value_ab(board, depth, alpha, beta):
    """
    Maximizing Player.
    :param board: current board state;
    :param depth: current depth;
    :return: returns the best value.
    """
    value = board.utility()
    if depth == 0 or value in [-512, 512] or board.is_draw():
        return value
    v = float("-inf")
    for s in successors(board, pc):
        v = max(v, min_value_ab(s, depth - 1, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v
    

def player_player(board):
    """
    Function that initializes the player vs player mode.
    :param board: Empty board;
    """
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
                        print("Column %d is full!" % column)
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
                        print("Column %d is full!" % column)


def player_pc(board):
    """
    Function that initializes the player vs pc mode.
    :param board: Empty board;
    """
    global max_depth
    global n_nodes
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
                        print("Column %d is full!" % column)
        else:
            print("PC turn.")
            start = time.time()
            if ai == "1":
                b = min_max(board, depth)
            else:
                b = alpha_beta(board, depth, float("-inf"), float("+inf"))
            if board.play(b, pc):
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
                print("ERROR!")
                print("Column %d is full!" % b)
                print("AI has no possible moves.")
                break
            end = time.time()
            memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
            print("Time to play: %f s" % (end - start))
            print("Memory used: %s MB" % memory)
            print("Number of generated nodes: %d" % n_nodes)


def pc_pc(board):
    """
    Function that initializes the pc vs pc mode.
    :param board: Empty board;
    """
    global max_depth
    global n_nodes
    print("1: AI - MiniMax")
    print("2: AI - Alpha-Beta")
    ai = input("Option: ")
    print("Difficulty:")
    print("Depth: 4 (Easy)  Depth: 6 (Medium)  Depth: 8 (Hard)")
    depth = int(input("Depth: "))
    max_depth = depth
    print("1: PC 1")
    print("2: PC 2")
    plays_first = input("Who plays first? [1/2]: ")
    pc_turn = True

    if plays_first == "1":
        pc_turn = False

    board.print_board()
    print("PC 1 is 'X' and PC 2 is 'O'")
    while True:
        if not pc_turn:
            print("PC 1 turn.")
            start = time.time()
            if ai == "1":
                b = min_max(board, depth)
            else:
                b = alpha_beta(board, depth, float("-inf"), float("+inf"))
            if board.play(b, pc):
                board.print_board()
                if board.is_draw():
                    who_won(0, pc)
                    break
                result = board.utility()
                if result in [-512, 512]:
                    who_won(result, pc)
                    break
                pc_turn = True
            else:
                print("There are no possible win moves.")
                print("Draw!")
                break
            end = time.time()
            memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
            print("Time to play: %f s" % (end - start))
            print("Memory used: %s MB" % memory)
            print("Number of generated nodes: %d" % n_nodes)
            n_nodes = 0
        else:
            print("PC 2 turn.")
            start = time.time()
            if ai == "1":
                b = min_max(board, depth)
            else:
                b = alpha_beta(board, depth, float("-inf"), float("+inf"))
            if board.play(b, pc2):
                board.print_board()
                if board.is_draw():
                    who_won(0, pc2)
                    break
                result = board.utility()
                if result in [-512, 512]:
                    who_won(result, pc2)
                    break
                pc_turn = False
            else:
                print("There are no possible win moves.")
                print("Draw!")
                break
            end = time.time()
            memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
            print("Time to play: %f s" % (end - start))
            print("Memory used: %s MB" % memory)
            print("Number of generated nodes: %d" % n_nodes)
            n_nodes = 0


def start_game(option):
    board = Board()
    if option == 1:
        player_player(board)
    elif option == 2:
        player_pc(board)
    else:
        pc_pc(board)
        

def main():
    print("Connect Four:")
    print("1: Player vs Player")
    print("2: Player vs PC")
    print("3: PC vs PC")
    option = int(input("Option: "))
    start_game(option)


if __name__ == '__main__':
    main()
