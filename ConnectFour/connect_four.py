#!/usr/bin/env python3

"""
minmax() {
    if jog terminal return +512, -512
    if lin pref return util(jog)  (min/max??)
    for(i = 0; i < 7; i++) {
        joga(i)
        v = min/max 
    }
    return v;
}

while not end game
    v = infinito
    if compplaysfirst
        for(i = 0; i < 7; i++) {
            v = maximo(v, max(tabuleiro))
            play = i
        }
        jogada(play)
    else pedejogada 
"""
player1 = 0
player2 = 1
pc = 3


class Board:
    width = 7
    height = 6

    def __init__(self):
        self.board = [["_" for j in range(self.width)] for i in range(
            self.height)]


    def play(self, column, player):
        placed = False
        for i in range(self.height-1, -1, -1):
            if self.board[i][column] == "_":
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
        for i in range(0, self.height):  #HORIZONTAL
            for j in range(0, self.width):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 2
            cont = 0
        
        cont = 0
        for j in range(0, self.width):  #VERTICAL
            for i in range(0, self.height):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 2
            cont = 0
        
        cont = 0
        i = 0
        for side in range(3, -1, -1):  #DIAGONAL RIGHT
            for j in range(side, self.width):
                if self.board[i][j] == play:
                    cont += 1
                else:
                    cont = 0
                if cont == 4:
                    return 2
                i += 1
                if(i == 6):
                    break
            cont = 0
            i = 0

        cont = 0
        j = 0
        for side in range(2, -1, -1):  # DIAGONAL LEFT
            for i in range(side, self.height):
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

        return 0
    #dentro da utilidade
    #def utility(self, i, j):


    def print_board(self):
        print("  0 1 2 3 4 5 6")
        print(" _______________")
        for i in range(self.height):
            str = "|"
            for j in range(self.width):
                str += " " + self.board[i][j]
            print(str + " |")
        print(" ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")


def who_won(result, player):
    if player == player1:
        if result == 1:
            print("Draw!")        
        elif result == 2:
            print("You Won!")
        else:
            print("You Lost!")
    elif player == player2:
        if result == 1:
            print("Draw!")
        elif result == 2:
            print("Player2 Won!")
        else:
            print("Player2 Lost!")
    else:
        if result == 1:
            print("Draw!")        
        elif result == 2:
            print("PC Won!")
        else:
            print("PC Lost!")
    

def start_game(option):
    board = Board()
    board.print_board()
    
    plays_first = input("Do you want to play first? [y/n]: ")
    pc_turn = True
    
    if plays_first == "y" or plays_first ==  "yes":
        pc_turn = False
        
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
                if result != 0:
                    who_won(result, player1)
                    break
                pc_turn = True
        else:
            print("PC turn.")
            column = int(input("Choose column: "))
            board.play(column, pc)
            board.print_board()
            result = board.finished(pc)
            if result != 0:
                who_won(result, pc)
                break
            pc_turn = False


def main():
    print("1: Player vs Player")
    print("2: Player vs PC")
    option = input("Option: ")
    start_game(option)


if __name__ == '__main__':
    main()
