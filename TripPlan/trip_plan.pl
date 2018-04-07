:- op(50, xfy, :).
:- use_module(library(lists)).

:-include("db.pl").

flight(Place1, Place2, Day, Flight_num, Dep_time, Arr_time) :-
    timetable(Place1, Place2, Flight_list),
    member(Dep_time/Arr_time/Flight_num/Day_list, Flight_list),
    travel_days(Day, Day_list).

travel_days(Day, Day_list) :- member(Day, Day_list).
travel_days(Day, alldays) :- member(Day, [su, mo, tu, we, th, fr, sa]).

next_day(su, mo).
next_day(mo, tu).
next_day(tu, we).
next_day(we, th).
next_day(th, fr).
next_day(fr, sa).
next_day(sa, su).

deptime([_-_:_:Dep_time|_], Dep_time).

transfer(Hr1:Min1, Hr2:Min2) :- 60 * (Hr2 - Hr1) + (Min2 - Min1) >= 40.

direct_flights(Place1, Place2, Day) :-
    travel_days(alldays, Day),
    flight(Place1, Place2, Day, _, _, _).

route(Place1, Place2, Day, [Place1-Place2:Flight_num:Dep_time]) :-
    flight(Place1, Place2, Day, Flight_num, Dep_time, _).

route(Place1, Place2, Day, [(Place1-Place3:Flight_num1:Dep_time1)|Rest_Route]) :-
    route(Place3, Place2, Day, Rest_Route),
    flight(Place1, Place3, Day, Flight_num1, Dep_time1, Arr_time1),
    deptime(Rest_Route, Dep_time2),
    transfer(Arr_time1, Dep_time2).

multiple_cities(Place1, Day, Cities, Route) :- 
    multiple_cities_aux(Place1, Place1, Day, Cities, Route).

multiple_cities_aux(Place2, Place1, Day, [], [Place1-Place2:Flight_num:Day:Dep_time]) :-
    flight(Place1, Place2, Day, Flight_num, Dep_time, _).

multiple_cities_aux(Place2, Place1, Day, Rest_Days, [(Place1-Next_City:Flight_num1:Day:Dep_time1)|Rest_Route]) :-
    member(Next_City, Rest_Days),
    flight(Place1, Next_City, Day, Flight_num1, Dep_time1, _),
    next_day(Day, NextDay),
    delete(Rest_Days, Next_City, Rest_Days_Aux),
    multiple_cities_aux(Place2, Next_City, NextDay, Rest_Days_Aux, Rest_Route).
