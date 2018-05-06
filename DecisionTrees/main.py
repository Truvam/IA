#!/usr/bin/env python3


import csv
import glob
import sys
from prettytable import PrettyTable
from decision_tree import id3
frequency = {}


class Data:
    def __init__(self, name, header, rows):
        self.name = name
        self.attributes = header
        self.values = rows
        self.length = len(rows)

    def print_data(self):
        print(self.name)
        table = PrettyTable(self.attributes)
        for row in self.values:
            table.add_row(row)
        print(table)


def find_files(argv=None):
    if argv is None:
        argv = glob.glob('./*.csv')
        if len(argv) == 0:
            print("No csv files found.")
            exit()
        else:
            d = {i: argv[i] for i in range(len(argv))}
            print("Files found: ", d)
            n = int(input("Choose number of file: "))
            data = load_csv(argv[n])
            return data
    else:
        data = load_csv(argv[0])
        return data


def load_csv(file):
    print("Loading csv file: " + file)
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        content = list(reader)
    data = Data(file, content[0], content[1:])
    return data


def count_value(values, attributes, key):
    attr_index = attributes.index(key)
    for val in values:
        if (key, val[attr_index], val[-1]) in frequency:
            frequency[(key, val[attr_index], val[-1])] += 1
        else:
            frequency[(key, val[attr_index], val[-1])] = 1


def print_tree(values, attributes, tree, level=0, before=""):
    if not tree or len(tree) == 0:
        print("\t" * level, "-")
    else:
        key_before = ""
        for key, value in tree.items():
            if isinstance(value, dict):
                if key in attributes:
                    print("\t" * level, "<" + key + ">:")
                    count_value(values, attributes, key)
                    key_before = key
                else:
                    print("\t" * level, key + ":")
                # print(frequency)
                print_tree(values, attributes, value, level+1, key_before)
            else:
                print("\t" * level, key + ":", value,
                      "(" + str(frequency[(before, key, value)]) + ")")


def main():
    if len(sys.argv) > 1:
        data = find_files(argv=sys.argv[1:])
    else:
        data = find_files()
    data.print_data()

    target_attr = data.attributes[-1]
    tree = id3(data.values, data.attributes, target_attr)

    print_tree(data.values, data.attributes, tree)


if __name__ == "__main__":
    main()
