% :- = IF
:- use_module(library(lists)).
% member: True if Elem is member of List


route(Place1, Place2, Day, Route).

flight(Place1, Place2, Day, Flight_num, Dep_time, Arr_time) :-
    timetable(Place1, Place2, Flights),
    member(Dep_time/Arr_time/Flight_num/Days, Flights),
    traveldays(Days, Day).

talveldays(Days, Day) :- member(Day, Days).
traveldays(alldays, Day) :- member(Day, alldays).

deptime(Route, Time).

transfer(Time1, Time2). :- (Time2 - Time1) * 60 >= 40.



