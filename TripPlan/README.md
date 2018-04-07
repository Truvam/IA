[![python](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/)

# Trip Plan
## Installation:
```
Version: Python 3.5.2 | SWI-Prolog 7.2.3
$ git clone https://github.com/Truvam/IA.git
$ cd IA/TripPlan/
$ sudo pip3 install -r requirements.txt
```
## Example Python:
### `Input:`
```
$ python3 trip_plan.py
Trip Plan:
Database connected!
  Available destinations:
+-----------+-------------+
|  Starting | Destination |
+-----------+-------------+
| edinburgh |    london   |
|   london  |  edinburgh  |
|   london  |  ljubljana  |
|   london  |    zurich   |
|   london  |    milan    |
| ljubljana |    zurich   |
| ljubljana |    london   |
|   milan   |    zurich   |
|   milan   |    london   |
|   zurich  |    milan    |
|   zurich  |  ljubljana  |
|   zurich  |    london   |
+-----------+-------------+
1: Which days there are direct flights from Place1 to Place2.
2: Available flights from Place1 to Place2.
3: Visit multiple cities.
Option: 3
Initial City: london
Available days: ['su', 'mo', 'tu', 'we', 'th', 'fr', 'sa']
Starting day: tu
Returning day: fr
How many cities do you need to visit? 2
Which cities do you need to visit?
City 1: ljubljana
City 2: zurich
```
### `Output:`
```
Available flights:

Starting : london
Destination: ljubljana
+----------------+--------------+---------------+------+
| Departure Time | Arrival Time | Flight Number | Days |
+----------------+--------------+---------------+------+
|     13:20      |    16:20     |     ju201     |  fr  |
|     13:20      |    16:20     |     ju213     |  su  |
+----------------+--------------+---------------+------+


Starting : ljubljana
Destination: zurich
+----------------+--------------+---------------+-------+
| Departure Time | Arrival Time | Flight Number |  Days |
+----------------+--------------+---------------+-------+
|     11:30      |    12:40     |     ju322     | tu,th |
+----------------+--------------+---------------+-------+


Starting : zurich
Destination: london
+----------------+--------------+---------------+-------------------+
| Departure Time | Arrival Time | Flight Number |        Days       |
+----------------+--------------+---------------+-------------------+
|      9:00      |     9:40     |     ba613     | mo,tu,we,th,fr,sa |
|     16:10      |    16:55     |     sr806     | mo,tu,we,th,fr,su |
+----------------+--------------+---------------+-------------------+


ROUTE: Starting: london ---> ljubljana ---> zurich ---> london :Destination
```
## Example ProLog:
```
$ swipl
?- [trip_plan].
?- direct_flights(edinburgh, london, su).
true .

?- route(ljubljana, edinburgh, th, R).
R = [ljubljana-zurich:ju322:11:30, zurich-london:sr806:16:10, london-edinburgh:ba4822:18:40] .

?- multiple_cities(london, tu, [milan, ljubljana, zurich], R).
R = [london-milan:ba510:tu:8:30, milan-zurich:sr621:we:9:25, 
zurich-ljubljana:yu323:th:13:30, ljubljana-london:yu200:fr:11:10].
