#!/usr/bin/env python3


import csv
import glob
import sys
from prettytable import PrettyTable
from decision_tree import id3, classify
import pydot
frequency = {}
graph = None


class Data:
    def __init__(self, name, header, rows):
        self.name = name
        self.attributes = header
        self.values = rows
        self.length = len(rows)

    def print_data(self, data=None, test=None):
        print(self.name)
        table = PrettyTable(self.attributes)
        for row in self.values:
            table.add_row(row)
        if data and test:
            table.add_column(data.attributes[-1], test)
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


def draw(parent, child, label=""):
    global graph
    edge = pydot.Edge(parent, child)
    edge.set_label(label)
    graph.add_edge(edge)


def print_tree(values, attributes, tree, level=0, parent=None, label=""):
    if not tree or len(tree) == 0:
        print("\t" * level, "-")
    else:
        for key, value in tree.items():
            if isinstance(value, dict):
                if key in attributes:
                    print("\t" * level, "<" + key + ">:")
                    count_value(values, attributes, key)
                    if parent and graph:
                        draw(parent, key, label)
                else:
                    print("\t" * level, key + ":")
                    label = key
                    key = parent
                print_tree(values, attributes, value, level+1, key, label)
            else:
                print("\t" * level, key + ":", value,
                      "(" + str(frequency[(parent, key, value)]) + ")")
                if graph:
                    draw(parent, value + " (" +
                         str(frequency[(parent, key, value)]) + ")", label=key)


def main():
    if len(sys.argv) > 1:
        data = find_files(argv=sys.argv[1:])
    else:
        data = find_files()
    data.print_data()

    target_attr = data.attributes[-1]
    tree = id3(data.values, data.attributes, target_attr)

    op = input("Do you want to create picture of tree graph? [y/n]: ")
    if op in 'yY' or op in 'yesYes':
        global graph
        graph = pydot.Dot(graph_type='graph')
        print_tree(data.values, data.attributes, tree)
        f_name = data.name.split('.')[1][1:] + '.png'
        graph.write_png(f_name)
        print("Generated graph to file:", f_name)
    else:
        print_tree(data.values, data.attributes, tree)

    op = input("Do you want to classify new examples? [y/n]: ")
    if op in 'yY' or op in 'yesYes':
        test_data = find_files()
        if test_data.attributes != data.attributes[:-1]:
            test_data.values.insert(0, test_data.attributes)
            test_data.attributes = data.attributes[:-1]
        try:
            class_results = classify(tree, test_data.values,
                                     test_data.attributes)
            test_data.print_data(data=data, test=class_results)
        except ValueError:
            print("Unable to classify examples in:", test_data.name)
            exit(0)


if __name__ == "__main__":
    main()
