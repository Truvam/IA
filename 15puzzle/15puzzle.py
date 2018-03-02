#!/usr/bin/env python3


from prettytable import PrettyTable
import math
import time
import resource
from queue import PriorityQueue


puzzle_size = 16
n_nodes = 0


class Node:
    def __init__(self, state, parent, operator, depth, path_cost):
        self.state = state
        self.parent = parent
        self.children = list()
        self.operator = operator
        self.depth= depth
        self.path_cost = path_cost


    def __lt__(self, other):
        return self.path_cost < other.path_cost


    def is_samePuzzle(self, state):
        """
        This compares two states, in order to verify if they are equal,
        it is also used to verify if the given state is the goal state.
        :param state: state to compare;
        :return: returns True or False whether the given states are equal.
        """
        if self.state == state:
            return True
        else:
            return False


    def move(self):
        """
        This function is used to create the children.
        For that it checks if the moves are possible and creates the
        respective children node.
        """
        new_state = self.state[:]
        blank_index = self.state.index(0)
        global n_nodes

        if blank_index not in [0, 1, 2, 3]: # UP
            tmp = new_state[blank_index - 4]
            new_state[blank_index - 4] = new_state[blank_index]
            new_state[blank_index] = tmp
            child = Node(new_state, self, "Up", self.depth + 1, self.path_cost)
            self.children.append(child)
            n_nodes += 1

        new_state = self.state[:]
        if blank_index not in [12, 13, 14, 15]:  # DOWN
            tmp = new_state[blank_index + 4]
            new_state[blank_index + 4] = new_state[blank_index]
            new_state[blank_index] = tmp
            child = Node(new_state, self, "Down", self.depth + 1, self.path_cost)
            self.children.append(child)
            n_nodes += 1

        new_state = self.state[:]
        if blank_index not in [0, 4, 8, 12]:  # LEFT
            tmp = new_state[blank_index - 1]
            new_state[blank_index - 1] = new_state[blank_index]
            new_state[blank_index] = tmp
            child = Node(new_state, self, "Left", self.depth + 1, self.path_cost)
            self.children.append(child)
            n_nodes += 1

        new_state = self.state[:]
        if blank_index not in [3, 7, 11, 15]:  # RIGHT
            tmp = new_state[blank_index + 1]
            new_state[blank_index + 1] = new_state[blank_index]
            new_state[blank_index] = tmp
            child = Node(new_state, self, "Right", self.depth + 1, self.path_cost)
            self.children.append(child)
            n_nodes += 1


def print_puzzle(state):
    """
    Prints the matrix of the desired state.
    :param state: state to print.
    """
    table = PrettyTable()
    table.add_row(state[0:4])
    table.add_row(state[4:8])
    table.add_row(state[8:12])
    table.add_row(state[12:16])
    print(table)


def create_menu(option):
    """
    Creates the strategies and heuristics menu.
    :param option: receives different option to create the strategies
    menu or the heuristics.
    """
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
    for i in range(0, puzzle_size):
        for j in range(i+1, puzzle_size):
            if config[i] > config[j] and config[j] != 0:
                n_inv += 1
    return (blank_row % 2 != 0) == (n_inv % 2 == 0)
    

def DFS(initialConfig, finalConfig):
    """
    Depth-first search Algorithm.
    :param initialConfig: initial state;
    :param finalConfig: goal state.
    """
    stack = list()
    stack.append(Node(initialConfig, None, "", 0, 0))
    visited = list()
    GoalFound = False
    max_depth = 15

    while stack and not GoalFound:
        node = stack.pop()
        visited.append(node)
        node.move()
        if max_depth > node.depth:
            for child in node.children:
                if child.is_samePuzzle(finalConfig):
                    print("Goal Found!")
                    GoalFound = True
                    path_solution(child)
                if not contains(stack, child) and not contains(visited, child):
                    stack.append(child)


def BFS(initialConfig, finalConfig):
    """
    Breadth-first search Algorithm.
    :param initialConfig: initial state;
    :param finalConfig: goal state.
    """
    queue = list()
    queue.append(Node(initialConfig, None, "", 0, 0))
    visited = list()
    GoalFound = False

    while queue and not GoalFound:
        node = queue.pop(0)
        visited.append(node)
        node.move()
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
            if not contains(queue, child) and not contains(visited, child):
                queue.append(child)


def IDFS(initialConfig, finalConfig):
    """
    Iterative deepening depth-first search Algorithm.
    :param initialConfig: initial state;
    :param finalConfig: goal state.
    """
    depth = 0
    GoalFound = False
    while not GoalFound:
        if DLS(initialConfig, finalConfig, depth):
            GoalFound = True
        depth += 1


def DLS(initialConfig, finalConfig, depth):
    """
    Depth-limited search Algorithm, used with IDFS.
    :param initialConfig: initial state;
    :param finalConfig: goal state;
    :param depth: current depth received from IDFS;
    :return: returns True or False, whether goal state was found.
    """
    stack = list()
    stack.append(Node(initialConfig, None, "", 0, 0))
    visited = list()
    GoalFound = False

    while stack:
        node = stack.pop()
        visited.append(node)
        node.move()
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
    """
    Best-first search: Greedy Algorithm.
    :param initialConfig: initial state;
    :param finalConfig: final state;
    :param heuristic: the heuristic chosen on menu.
    """
    pq = PriorityQueue()
    pq.put(Node(initialConfig, None, "", 0, 0))
    visited = list()
    GoalFound = False

    while pq and not GoalFound:
        node = pq.get()
        visited.append(node)
        node.move()
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
            if not contains(pq.queue, child) and not contains(visited, child):
                if heuristic == '1':
                    cost = heuristic_misplace(child.state, finalConfig)
                    child.path_cost = cost
                else:
                    cost = heuristic_manhattan(child.state, finalConfig)
                    child.path_cost = cost
                pq.put(child, cost)


def A_Star(initialConfig, finalConfig, heuristic):
    """
    Best-first search: A* Algorithm.
    :param initialConfig: initial state;
    :param finalConfig: final state;
    :param heuristic: the heuristic chosen on menu.
    """
    pq = PriorityQueue()
    pq.put(Node(initialConfig, None, "", 0, 0))
    GoalFound = False

    while pq and not GoalFound:
        node = pq.get()
        node.move()
        for child in node.children:
            if child.is_samePuzzle(finalConfig):
                print("Goal Found!")
                GoalFound = True
                path_solution(child)
            if heuristic == '1':
                cost = child.depth + heuristic_misplace(child.state,
                                                        finalConfig)
                child.path_cost = cost
            else:
                cost = child.depth + heuristic_manhattan(child.state, 
                                                         finalConfig)
                child.path_cost = cost
            pq.put(child, cost)


def heuristic_manhattan(state, finalConfig):
    """
    Manhattan distance heuristic, the heuristic sums the distances of each
    piece to its place in the final state.
    :param state: current state;
    :param finalConfig: final state;
    :return: sum of all distances.
    """
    cont = 0
    for i in range(0, 16):
        cont += manhattan_aux(state.index(i), finalConfig.index(i))
    return cont


def manhattan_aux(i, j):
    """
    This is a auxiliary function to manhattan distance.
    :param i: index of piece in the current state list;
    :param j: index of piece in the final state list;
    :return: returns number of moves that are necessary to put the piece in
    the same place as its final state.
    """
    # Used to obtain the matrix coordinates from the state list.
    matrix_ij = {0: (1, 1), 0.25: (1, 2), 0.50: (1, 3), 0.75: (1, 4),
                 1: (2, 1), 1.25: (2, 2), 1.50: (2, 3), 1.75: (2, 4),
                 2: (3, 1), 2.25: (3, 2), 2.50: (3, 3), 2.75: (3, 4),
                 3: (4, 1), 3.25: (4, 2), 3.50: (4, 3), 3.75: (4, 4)}

    x1, y1 = matrix_ij[i/4]
    x2, y2 = matrix_ij[j/4]
    return abs(x1-x2) + abs(y1-y2)


def heuristic_misplace(state, finalConfig):
    """
    This heuristics checks the number of out of place pieces.
    :param state: current state;
    :param finalConfig: goal state;
    :return: returns the number of out of place pieces.
    """
    h = 0
    for i in range(0, 16):
        if state[i] != finalConfig[i]:
            h += 1
    return h


def contains(listNode, Node):
    """
    This function checks if a certain state is present in a list of nodes.
    :param listNode: list of nodes;
    :param Node: current node;
    :return: returns True or False, whether the state was found on the list.
    """
    contains = False
    for node in listNode:
        if(node.is_samePuzzle(Node.state)):
            contains = True
    return contains


def path_solution(Node):
    """
    Prints the depth of the node, and goes to each parent node to obtain the
    operator needed to create the path to solution.
    :param Node: Node of the goal state.
    """
    node = Node
    directions = list()
    directions.append(node.operator)
    depth = node.depth
    while node.parent is not None:
        node = node.parent
        directions.append(node.operator)
    directions.pop()
    print("Path to solution: ", end="")
    print(directions)
    print("Depth: %d" % depth)


def execute(option, initialConfig, finalConfig, heuristic):
    """
    Function used to execute the algorithm and heuristic.
    In the end prints: Number of nodes created, time to finish and memory used.
    :param option: algorithm chosen from the menu;
    :param initialConfig: initial sate;
    :param finalConfig: final state;
    :param heuristic: heuristic chosen from the menu.
    """
    print("Finding Path to Solution...")
    start  = time.time()
    global n_nodes

    if option == '1':
        print("Using: DFS")
        DFS(initialConfig, finalConfig)
    elif option == '2':
        print("Using: BFS")
        BFS(initialConfig, finalConfig)
    elif option == '3':
        print("Using: IDFS")
        IDFS(initialConfig, finalConfig)
    elif option == '4':
        if heuristic == '1':
            print("Using: Greedy + Misplaced Pieces")
        else:
            print("Using: Greedy + Manhattan Distance")
        Greedy(initialConfig, finalConfig, heuristic)
    elif option == '5':
        if heuristic == '1':
            print("Using: A* + Misplaced Pieces")
        else:
            print("Using: A* + Manhattan Distance")
        A_Star(initialConfig, finalConfig, heuristic)

    end = time.time()
    memory = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000
    print("Number of generated nodes: %d" % n_nodes)
    print("Time to finish: %f s" % (end - start))
    print("Memory used: %s MB" % memory)


def main():
    initialConfig = list(map(int, input("Initial Configuration: ").split()))
    finalConfig = list(map(int, input("Final Configuration: ").split()))
    if not (has_solution(initialConfig) == has_solution(finalConfig)):
        print("This 15 puzzle has no solution.")
    else:
        print("This 15 puzzle has solution.")
        create_menu(1)
        option = input('Option: ')
        heuristic = 0
        if option not in ['1', '2', '3']:
            create_menu(2)
            heuristic = input('Option: ')
        execute(option, initialConfig, finalConfig, heuristic)


if __name__ == '__main__':
    main()

