#!/usr/bin/env python3


import re
from prettytable import PrettyTable


class Flights:
    def __init__(self, departure, arrival, number, days):
        self.departureTime = departure
        self.arrivalTime = arrival
        self.flightNumber = number
        self.listDays = days


class Route:
    def __init__(self, place1, place2, list_flights):
        self.Place1 = place1
        self.Place2 = place2
        self.Flights = list()
        j = 0
        for i in range(len(list_flights)):
            v1 = list_flights[i][j]
            v2 = list_flights[i][j+1]
            v3 = list_flights[i][j+2]
            v4 = list_flights[i][j+3]
            flights = Flights(v1, v2, v3, v4)
            self.Flights.append(flights)


class Database:
    def __init__(self):
        self.Route = list()

    def connect(self):
        try:
            file = open("db.pl", "r")
            place1 = ""
            place2 = ""
            flights = list()
            i = 0
            for line in file:
                places = re.search("(?<=timetable\().*[a-zA-Z]", line)
                if places is not None:
                    place1, place2 = places.group().split(",")
                elif line != "\n":
                    v = re.search("\d.*[a-zA-Z]", line).group()
                    v = v.split("/")
                    v[3] = re.search("[a-zA-Z].*", v[3]).group()
                    flights.append(v)
                if "." in line:
                    routes = Route(place1, place2, flights)
                    self.Route.append(routes)
                    flights.clear()
                    i += 1
            return True
        except Exception as e:
            print(str(e))
            return False

    def print_database(self, place1=None, place2=None):
        found = False
        for route in self.Route:
            if route.Place1 == place1 and route.Place2 == place2 or place1 is\
                    None and place2 is None:
                print("Starting : " + route.Place1)
                print("Destination: " + route.Place2)
                table = PrettyTable(["Departure Time", "Arrival Time", "Flight "
                                                                       "Number",
                                     "Days"])
                for i in range(len(route.Flights)):
                    table.add_row([route.Flights[i].departureTime,
                                   route.Flights[
                        i].arrivalTime, route.Flights[i].flightNumber,
                                   route.Flights[i].listDays])
                print(table)
                print()
                found = True
        return found


def direct_flights(place1, place2, db):
    if not db.print_database(place1=place1, place2=place2):
        print("No direct flights from " + place1 + " to " + place2 + ".")


def main():
    print("Trip Plan:")
    db = Database()
    if db.connect():
        print("Database connected!")
        # db.print_database()
    else:
        exit()

    print("1: Which days there are direct flights from Place1 to Place2.")
    print("2: Available flights from Place1 to Place2.")
    print("3: Visit multiple cities.")
    option = int(input("Option: "))

    if option == 1:
        place1 = input("Place1: ")
        place2 = input("Place2: ")
    elif option == 2:
        place1 = input("Place1: ")
        place2 = input("Place2: ")
        direct_flights(place1, place2, db)
    else:
        cities = list()
        initial_city = input("Initial City: ")
        start_day = input("Starting day: ")
        return_day = input("Returning day: ")
        n = int(input("How many cities do you want to visit? "))
        print("Which cities do you want to visit?")
        for i in range(n):
            city = input("City %d: " % (i + 1))
            cities.append(city)


if __name__ == "__main__":
    main()
