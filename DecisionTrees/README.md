[![python](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/)

# Decision Trees
## Installation:
```
Version: Python 3.5.2  |  graphviz 2.38.0
$ git clone https://github.com/Truvam/IA.git
$ cd IA/DecisionTrees/
$ sudo pip3 install -r requirements.txt
$ sudo apt-get install graphviz
```
## Example:
```
$ python3 main.py restaurant.csv restaurant_test.csv
```
### `OR:`
```
$ python3 main.py
Files found:  {0: './iris.csv', 1: './restaurant.csv', 2: './restaurant_test.csv', 3: './weather.csv'}
Choose number of file: 1
Loading csv file: ./restaurant.csv
./restaurant.csv
+-----+-----+-----+-----+-----+------+-------+------+-----+---------+-------+-------+
|  ID | Alt | Bar | Fri | Hun | Pat  | Price | Rain | Res |   Type  |  Est  | Class |
+-----+-----+-----+-----+-----+------+-------+------+-----+---------+-------+-------+
|  X1 | Yes |  No |  No | Yes | Some |  $$$  |  No  | Yes |  French |  0-10 |  Yes  |
|  X2 | Yes |  No |  No | Yes | Full |   $   |  No  |  No |   Thai  | 30-60 |   No  |
|  X3 |  No | Yes |  No |  No | Some |   $   |  No  |  No |  Burger |  0-10 |  Yes  |
|  X4 | Yes |  No | Yes | Yes | Full |   $   |  No  |  No |   Thai  | 10-30 |  Yes  |
|  X5 | Yes |  No | Yes |  No | Full |  $$$  |  No  | Yes |  French |  >60  |   No  |
|  X6 |  No | Yes |  No | Yes | Some |   $$  | Yes  | Yes | Italian |  0-10 |  Yes  |
|  X7 |  No | Yes |  No |  No | None |   $   | Yes  |  No |  Burger |  0-10 |   No  |
|  X8 |  No |  No |  No | Yes | Some |   $$  | Yes  | Yes |   Thai  |  0-10 |  Yes  |
|  X9 |  No | Yes | Yes |  No | Full |   $   | Yes  |  No |  Burger |  >60  |   No  |
| X10 | Yes | Yes | Yes | Yes | Full |  $$$  |  No  | Yes | Italian | 10-30 |   No  |
| X11 |  No |  No |  No |  No | None |   $   |  No  |  No |   Thai  |  0-10 |   No  |
| X12 | Yes | Yes | Yes | Yes | Full |   $   |  No  |  No |  Burger | 30-60 |  Yes  |
+-----+-----+-----+-----+-----+------+-------+------+-----+---------+-------+-------+
Do you want to create picture of tree graph? [y/n]: y
 <Pat>:
         Full:
                 <Hun>:
                         No: No (4)
                         Yes:
                                 <Type>:
                                         Thai:
                                                 <Fri>:
                                                         No: No (3)
                                                         Yes: Yes (2)
                                         Burger: Yes (2)
                                         Italian: No (1)
         None: No (2)
         Some: Yes (4)
Generated graph to file: restaurant.png
Do you want to classify new examples? [y/n]: y
Files found:  {0: './iris.csv', 1: './restaurant.csv', 2: './restaurant_test.csv', 3: './weather.csv'}
Choose number of file: 2
Loading csv file: ./restaurant_test.csv
./restaurant_test.csv
+-----+-----+-----+-----+-----+------+-------+------+-----+---------+-------+-------+
|  ID | Alt | Bar | Fri | Hun | Pat  | Price | Rain | Res |   Type  |  Est  | Class |
+-----+-----+-----+-----+-----+------+-------+------+-----+---------+-------+-------+
|  X1 | Yes |  No |  No | Yes | Some |  $$$  |  No  | Yes |  French |  0-10 |  Yes  |
|  X2 | Yes |  No |  No | Yes | Some |   $   |  No  |  No |   Thai  | 30-60 |  Yes  |
|  X3 |  No | Yes |  No |  No | Some |   $   |  No  |  No |  Burger |  0-10 |  Yes  |
|  X4 |  No |  No | Yes | Yes | Full |   $   |  No  |  No |   Thai  | 10-30 |  Yes  |
|  X5 |  No |  No | Yes |  No | Full |  $$$  |  No  | Yes |  French |  >60  |   No  |
|  X6 |  No | Yes |  No | Yes | Some |   $$  | Yes  | Yes | Italian |  0-10 |  Yes  |
|  X7 |  No | Yes |  No |  No | None |   $   | Yes  |  No |  Burger |  0-10 |   No  |
|  X8 |  No |  No |  No | Yes | Some |   $$  | Yes  | Yes |   Thai  |  0-10 |  Yes  |
|  X9 |  No | Yes | Yes |  No | None |   $   | Yes  |  No |  Burger |  >60  |   No  |
| X10 | Yes | Yes | Yes | Yes | Full |  $$$  |  No  | Yes | Italian | 10-30 |   No  |
| X11 |  No |  No |  No |  No | None |   $   |  No  |  No |   Thai  |  0-10 |   No  |
| X12 | Yes | Yes | Yes | Yes | Full |   $   |  No  |  No |  Burger | 30-60 |  Yes  |
+-----+-----+-----+-----+-----+------+-------+------+-----+---------+-------+-------+