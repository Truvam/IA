#!/usr/bin/env python3


from prettytable import PrettyTable
#from memory_profiler import memory_usage #not needed, replaced by resource
import math
import time
import resource
from queue import PriorityQueue


puzzle_size = 16
n_nodes = 0


class Node:
    def __init__(self, state, parent, operator, depth, path_cost):
        self.state = state  #array from puzzle
        self.parent = parent
        self.children = list() #needs to be a list of nodes
        self.operator = operator
        self.depth= depth
        self.path_cost = path_cost

    
    #Priority Queue needs to be able to order by path cost
    def __lt__(self, other):
        return self.path_cost < other.path_cost


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
            child = Node(new_state, self, "Up", self.depth + 1, self.path_cost)
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
            child = Node(new_state, self, "Down", self.depth + 1, self.path_cost)
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
            child = Node(new_state, self, "Left", self.depth + 1, self.path_cost)
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
            child = Node(new_state, self, "Right", self.depth + 1, self.path_cost)
            self.children.append(child)
            n_nodes += 1


def print_puzzle(state):
    table = PrettyTable()
    table.add_row(state[0:4])
    table.add_row(state[4:8])
    table.add_row(state[8:12])
    table.add_row(state[12:16])

    print(table)


def create_menu(option):
    if option == 1:
        table = PrettyTable(['Strategies', 'Options'])
        table.add_row(['DFS', 1])
        table.add_row(['BFS', 2])
        table.add_row(['IDFS', 3])
        table.add_row(['Greedy', 4])
        table.add_row(['A*', 5])
    else:
        table = PrettyTable(['Heuristics', 'Options'])
        table.add_row(['Number of out of place pieces', 1])
        table.add_row(['Manhattan Distance', 2])
    print(table)


def has_solution(config):
    """
    Function to check whether any game state is solvable.
    URL: https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
    Formula:
       a. If the grid width is odd, then the number of inversions in a solvable
       situation is even.
       b. If the grid width is even, and the blank is on an even row counting
       from the bottom (second-last, fourth-last etc), then the number of
       inversions in a solvable situation is odd.
       c. If the grid width is even, and the blank is on an odd row counting
       from the bottom (last, third-last, fifth-last etc) then the number of
       inversions in a solvable situation is even.
    :param config: configuration array;
    :return: returns true or false based on the formula specified above.
    """
    n_inv = 0
    blank_row = math.ceil((16 - config.index(0)) / 4)
    #print("Blank Row: %d" % blank_row)
    for i in range(0, puzzle_size):
        for j in range(i+1, puzzle_size):
            if config[i] > config[j] and config[j] != 0:
                #print("%d %d" %(config[i], config[j]))
                n_inv += 1
    #print("number of inversions: %d" % n_inv)
    return (blank_row % 2 != 0) == (n_inv % 2 == 0)
    

def DFS(initialConfig, finalConfig): #verificar se o no ja existe
    stack = list()
    stack.append(Node(initialConfig, None, "", 0, 0))
    visited = list()
    #path_solution = list()
    GoalFound = False
    max_depth = 15
    while stack and not GoalFound:
        node = stack.pop()
        visited.append(node)
        node.move()
        #print_puzzle(node.state)
        #try to do moves at random order, to solve the depth problem
        if max_depth > node.depth:
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
    queue.append(Node(initialConfig, None, "", 0, 0))
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


def IDFS(initialConfig, finalConfig):
    depth = 0
    GoalFound = False
    while not GoalFound:
        if DLS(initialConfig, finalConfig, depth):
            GoalFound = True
        depth += 1


def DLS(initialConfig, finalConfig, depth):
    stack = list()
    stack.append(Node(initialConfig, None, "", 0, 0))
    visited = list()
    GoalFound = False
    while stack:
        node = stack.pop()
        visited.append(node)
        node.move()
        # print_puzzle(node.state)
        if depth > node.depth:
            for child in node.children:
                if child.is_samePuzzle(finalConfig):
                    print("Goal Found!")
                    GoalFound = True
                    path_solution(child)
                    return GoalFound
                if not contains(stack, child) and not contains(visited, child):
                    stack.append(child)
    return GoalFound


def Greedy(initialConfig, finalConfig, heuristic):
    pq = PriorityQueue()
    node = Node(initialConfig, None, "", 0, 0)
    #print_puzzle(node.state)
    
    if heuristic == '1':
        cost = node.depth + heuristic_place(node.state, finalConfig)
    else:
        cost = node.depth + heuristic_manhattan(node.state, finalConfig)
    
    pq.put(node, cost)
    visited = list()
    GoalFound = False

    while pq and not GoalFound:
        node = pq.get()
        #visited.append(node)
        node.move()
        #print_puzzle(node.state)
        #print("cost: %d" % node.path_cost) 
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
            if not contains(pq.queue, child) and not contains(visited, child):
                if heuristic == '1':
                    cost = heuristic_place(child.state, finalConfig)
                    child.path_cost = cost
                else:
                    cost = heuristic_manhattan(child.state, finalConfig)
                    child.path_cost = cost
                pq.put(child, cost)


def A_Star(initialConfig, finalConfig, heuristic):
    pq = PriorityQueue()
    node = Node(initialConfig, None, "", 0, 0)
    #print_puzzle(node.state)
    
    if heuristic == '1':
        cost = node.depth + heuristic_place(node.state, finalConfig)
    else:
        cost = node.depth + heuristic_manhattan(node.state, finalConfig)
    
    pq.put(node, cost)
    visited = list()
    GoalFound = False

    while pq and not GoalFound:
        node = pq.get()
        #visited.append(node)
        node.move()
        #print_puzzle(node.state)
        #print("cost: %d" % node.path_cost) 
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
            if heuristic == '1':
                cost = child.depth + heuristic_place(child.state, finalConfig)
                child.path_cost = cost
            else:
                cost = child.depth + heuristic_manhattan(child.state, 
                                                         finalConfig)
                child.path_cost = cost
            pq.put(child, cost)


def heuristic_manhattan(state, finalConfig): #verificar se esta correto
    #print("Manhattan")
    cont = 0
    #print_puzzle(state)
    #print_puzzle(finalConfig)
    #tem que ser o numero de movimentos necessarios para chegar a posição correta
    for i in range(0, 15):
        n = finalConfig.index(i) - state.index(i)
        #print("N: %d" % n)
        cont += manhattan_aux(n)

    print(cont)
    return cont


def manhattan_aux(n):
    for j in range(-1, 15):
        for k in range(-1, 15):
            #print("J: %d + K: %d" % (j, k))
            #print("SUM: %d" % (j*4 + k*4))
            if (j*4 + k*1) == n:
                print("J: %d + K: %d" % (j, k))
                #print("Found")
                return abs(j + k)
    return 0


def heuristic_place(state, finalConfig):
    """
    This heuristics checks the number of out of place pieces.
    :param initialConfig: First state;
    :param finalConfig: Goal state;
    :return: returns the number of out of place pieces.
    """
    h = 0
    for i in range(0, 16):
        #print("%d %d" % (state[i], finalConfig[i]))
        if state[i] != finalConfig[i]:
            h += 1
    #print("h: %d" % h)
    return h


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
    directions.append(node.operator)
    #print_puzzle(node.state)
    #print(node.direction)
    depth = node.depth
    path_cost = node.path_cost
    while node.parent is not None:
        node = node.parent
        #print_puzzle(node.state)
        #print(node.direction)
        #path.append(node.parent)
        directions.append(node.operator)
    directions.pop()
    print("Path to solution: ", end="")
    print(directions)
    print("Depth: %d" % depth)
    print("Path Cost: %d" % path_cost)
    #print("Time to finish: ")
    #print("Memory used: ")
    #print("Depth/Cost: ")
    #return path


def execute(option, initialConfig, finalConfig, heuristic):
    print("Finding Path to Solution...")
    start  = time.time()
    global n_nodes

    if option == '1':
        print("DFS")
        DFS(initialConfig, finalConfig)
    elif option == '2':
        print("Using: BFS")
        BFS(initialConfig, finalConfig)
        # quantos movimentos sao necessarios para encontrar solução
    elif option == '3':
        print("IDFS")
        IDFS(initialConfig, finalConfig)
    elif option == '4':
        print("Greedy")
        Greedy(initialConfig, finalConfig, heuristic)
    elif option == '5':
        print("A*")
        A_Star(initialConfig, finalConfig, heuristic)

    end = time.time()
    memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
    print("Number of generated nodes: %d" % n_nodes)
    print("Time to finish: %f s" % (end - start))
    print("Memory used: %s MB" % memory)


def main():
    initialConfig = list(map(int, input("Initial Configuration: ").split()))
    finalConfig = list(map(int, input("Final Configuration: ").split()))
    #print(initialConfig)
    #print(finalConfig)
    if not (has_solution(initialConfig) == has_solution(finalConfig)):
        print("This 15 puzzle has no solution.")
    else:
        print("This 15 puzzle has solution.")
        create_menu(1)
        option = input('Option: ')
        create_menu(2)
        heuristic = input('Option: ')
        execute(option, initialConfig, finalConfig, heuristic)


if __name__ == '__main__':
    main()

