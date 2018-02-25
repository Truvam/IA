#!/usr/bin/env python3


from prettytable import PrettyTable
#from memory_profiler import memory_usage #not needed, replaced by resource
import math
import time
import resource
import heapq


puzzle_size = 16
n_nodes = 0


#lista de matrizes
class Node:
    def __init__(self, state, parent, direction):
        self.state = state  #array from puzzle
        self.parent = parent
        self.children = list() #needs to be a list of nodes
        self.direction = direction

    def is_samePuzzle(self, state):
        if self.state == state:
            return True
        else:
            return False


    def move(self):
        # position can be 1, 2, 3, 4 = up, down, left, right

        new_state = self.state[:]  # [:] is needed or original sate will be
        blank_index = self.state.index(0)
        global n_nodes
        # changed
        # print("State:")
        # print_puzzle(state)
        if blank_index not in [0, 1, 2, 3]: # UP
            tmp = new_state[blank_index - 4]
            new_state[blank_index - 4] = new_state[blank_index]
            new_state[blank_index] = tmp
            #print_puzzle(self.state)
            #print("Up")
            #print_puzzle(new_state)
            child = Node(new_state, self, "Up")
            self.children.append(child)
            n_nodes += 1

        new_state = self.state[:]
        if blank_index not in [12, 13, 14, 15]:  # DOWN
            tmp = new_state[blank_index + 4]
            new_state[blank_index + 4] = new_state[blank_index]
            new_state[blank_index] = tmp
            #print_puzzle(state)
            #print("Down")
            #print_puzzle(new_state)
            child = Node(new_state, self, "Down")
            self.children.append(child)
            n_nodes += 1

        new_state = self.state[:]
        if blank_index not in [0, 4, 8, 12]:  # LEFT
            tmp = new_state[blank_index - 1]
            new_state[blank_index - 1] = new_state[blank_index]
            new_state[blank_index] = tmp
            #print_puzzle(state)
            #print("Left")
            #print_puzzle(new_state)
            child = Node(new_state, self, "Left")
            self.children.append(child)
            n_nodes += 1

        new_state = self.state[:]
        if blank_index not in [3, 7, 11, 15]:  # RIGHT
            tmp = new_state[blank_index + 1]
            new_state[blank_index + 1] = new_state[blank_index]
            new_state[blank_index] = tmp
            #print_puzzle(state)
            #print("Right")
            #print_puzzle(new_state)
            child = Node(new_state, self, "Right")
            self.children.append(child)
            n_nodes += 1


def print_puzzle(state):
    table = PrettyTable()
    table.add_row(state[0:4])
    table.add_row(state[4:8])
    table.add_row(state[8:12])
    table.add_row(state[12:16])

    print(table)


def create_menu():
    table = PrettyTable(['Strategies', 'Options'])
    table.add_row(['DFS', 1])
    table.add_row(['BFS', 2])
    table.add_row(['IDFS', 3])
    table.add_row(['Greedy', 4])
    table.add_row(['A*', 5])
    print(table)


def has_solution(config):
    """
    Function to check whether any game state is solvable.
    Formula:
       a. If the grid width is odd, then the number of inversions in a solvable
       situation is even.
       b. If the grid width is even, and the blank is on an even row counting
       from the bottom (second-last, fourth-last etc), then the number of
       inversions in a solvable situation is odd.
       c. If the grid width is even, and the blank is on an odd row counting
       from the bottom (last, third-last, fifth-last etc) then the number of
       inversions in a solvable situation is even.
    :param config: configuration array
    :return: returns true or false based on the formula specified above.
    """
    n_inv = 0
    blank_row = math.ceil((16 - config.index(0)) / 4)
    print("Blank Row: %d" % blank_row)
    for i in range(0, puzzle_size):
        for j in range(i+1, puzzle_size):
            if config[i] > config[j] and config[j] != 0:
                #print("%d %d" %(config[i], config[j]))
                n_inv += 1
    print("number of inversions: %d" % n_inv)
    return (blank_row % 2 != 0) == (n_inv % 2 == 0)
    

def DFS(initialConfig, finalConfig): #verificar se o no ja existe
    stack = list()
    stack.append(Node(initialConfig, None, ""))
    visited = list()
    #path_solution = list()
    GoalFound = False
    while stack and not GoalFound:
        node = stack.pop()
        visited.append(node)
        node.move()
        #print_puzzle(node.state)
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
                #return path_solution
            if not contains(stack, child) and not contains(visited, child):
                stack.append(child)
    #return path_solution


def BFS(initialConfig, finalConfig): #verificar se o no ja existe
    queue = list()
    queue.append(Node(initialConfig, None, ""))
    visited = list()
    #path_solution = list()
    GoalFound = False
    while queue and not GoalFound:
        node = queue.pop(0)
        visited.append(node)
        node.move()
        #print_puzzle(node.state)
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
                #return path_solution
            if not contains(queue, child) and not contains(visited, child):
                queue.append(child)
    #return path_solution


def A_Star(initialConfig, finalConfig):
    heap = []
    heapq.heappush(heap, Node(initialConfig, None, ""))
    visited = list()
    GoalFound = False
    while heap and not GoalFound:
        node = heapq.heappop(heap)
        visited.append(node)
        node.move()
        print_puzzle(node.state)
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
                #return path_solution
            if not contains(heap, child) and not contains(visited, child):
                heapq.heappush(heap, child)
            elif child in heap:
                heapq.heappush(heap, child)
    #return path_solution


def contains(listNode, Node):
    contains = False
    for list in listNode:
        if(list.is_samePuzzle(Node.state)):
            contains = True
    return contains


def path_solution(Node):
    node = Node
    #path = list()
    #path.append(node)
    directions = list()
    directions.append(node.direction)
    #print_puzzle(node.state)
    #print(node.direction)
    n_moves = 0
    while node.parent is not None:
        node = node.parent
        #print_puzzle(node.state)
        #print(node.direction)
        #path.append(node.parent)
        directions.append(node.direction)
        n_moves += 1
    directions.pop()
    print("Path to solution: ", end="")
    print(directions)
    print("Number of moves: %d" % n_moves)
    #print("Time to finish: ")
    #print("Memory used: ")
    #print("Depth/Cost: ")
    #return path


def execute(option, initialConfig, finalConfig):
    print("Finding Path to Solution...")
    start  = time.time()
    global n_nodes

    if option == '1':
        print("DFS")
        # node = Node(initialConfig, None)
        # node.move()
        #memory = memory_usage((DFS, (initialConfig, finalConfig)))
        DFS(initialConfig, finalConfig)
    elif option == '2':
        print("Using: BFS")
        #memory = memory_usage((BFS, (initialConfig, finalConfig)),
        #                      max_usage=True, interval=0.0000001)
        BFS(initialConfig, finalConfig)
        # quantos movimentos sao necessarios para encontrar solução
    elif option == '3':
        print("IDFS")
    elif option == '4':
        print("Greedy")
    elif option == '5':
        print("A*")
        A_Star(initialConfig, finalConfig)

    end = time.time()
    memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
    print("Number of generated nodes: %d" % n_nodes)
    print("Time to finish: %f s" % (end - start))
    print("Memory used: %s MB" % memory)


def main():
    initialConfig = list(map(int, input("Initial Configuration: ").split()))
    finalConfig = list(map(int, input("Final Configuration: ").split()))
    print(initialConfig)
    print(finalConfig)
    if not (has_solution(initialConfig) == has_solution(finalConfig)):
        print("This 15 puzzle has no solution.")
    else:
        print("This 15 puzzle has solution.")
        create_menu()
        option = input('Option: ')
        execute(option, initialConfig, finalConfig)

main()

