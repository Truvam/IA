[![python](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/)

# 15 Puzzle
## Installation:
```
Version: Python 3.5.2
$ git clone https://github.com/Truvam/IA.git
$ cd IA/15puzzle/
$ sudo pip3 install -r requirements.txt
```
## Example:
### `Input:`
```
$ python3 15puzzle.py
Initial Configuration: 9 12 0 7 14 5 13 2 6 1 4 8 10 15 3 11
Final Configuration: 9 5 12 7 14 13 0 8 1 3 2 4 6 10 15 11
This 15 puzzle has solution.
+------------+---------+
| Strategies | Options |
+------------+---------+
|    DFS     |    1    |
|    BFS     |    2    |
|    IDFS    |    3    |
|   Greedy   |    4    |
|     A*     |    5    |
+------------+---------+
Option: 5
+-------------------------------+---------+
|           Heuristics          | Options |
+-------------------------------+---------+
| Number of out of place pieces |    1    |
|       Manhattan Distance      |    2    |
+-------------------------------+---------+
Option: 2
```
### `Output:`
```
Finding Path to Solution...
Using: A* + Manhattan Distance
Goal Found!
Path to solution: ['Up', 'Right', 'Right', 'Up', 'Left', 'Left', 'Down', 'Left', 'Down', 'Right', 'Right', 'Down', 'Left']
Depth: 13
Number of generated nodes: 506
Time to finish: 0.014251 s
Memory used: 9.688 MB
```
