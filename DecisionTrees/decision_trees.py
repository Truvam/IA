#!/usr/bin/env python3


import csv
import glob
import sys
from prettytable import PrettyTable


class Data:
    def __init__(self, name, header, rows):
        self.name = name
        self.header = header
        self.rows = rows

    def print_data(self):
        print(self.name)
        table = PrettyTable(self.header)
        for row in self.rows:
            table.add_row(row)
        print(table)


def find_files(argv=None):
    if argv is None:
        argv = glob.glob('./*.csv')
        if len(argv) == 0:
            print("No csv files found.")
            exit()
        else:
            print("Files found: ", end='')
            print(argv)
            op = input("Do you want to load them? [y/n]: ")
            if op in "yY" or op in "yesYes":
                data = load_csv(argv)
                return data
            else:
                print("Exiting...")
                exit()
    else:
        data = load_csv(argv)
        return data


def load_csv(argv):
    print("Loading csv files: ", end='')
    print(argv)
    data = list()
    for file in argv:
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            content = list(reader)
        data.append(Data(file, content[0], content[1:]))
    return data


def get_data(data):
    data[0].print_data()
    data[1].print_data()
    data[2].print_data()


def id3(examples, attributes, parent_examples):
    if examples is None:
        return plurality_value(parent_examples)
    elif same_classification(examples):
        return classification
    elif attributes is None:
        return plurality_value(examples)
    else:
        # A = argmax(a in attributes)importance(a, examples)
        # tree = new_decision_tree(test A)
        for value in vk(A):
            # exs = {e : e in examples and e.A = vk}
            subtree = id3(exs, attributes - A, examples)
            # tree.add_branch(label=(A = vk), subtree=subtree)
        return tree


def main():
    if len(sys.argv) > 1:
        data = find_files(argv=sys.argv[1:])
    else:
        data = find_files()
    get_data(data)


if __name__ == "__main__":
    main()
