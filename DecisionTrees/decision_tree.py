import math


class Node:
    def __init__(self, attribute, value, class_, counter):
        self.attribute = attribute
        self.value = value
        self.class_ = class_
        self.counter = counter


class DecisionTree:
    def __init__(self):
        self.Node = None
        self.examples = None
        self.attributes = None


def entropy(examples, target_attr):
    """
    Calculates the entropy of a examples set for the target attribute.
    :param examples: examples set
    :param target_attr: target attribute
    :return: returns the calculated entropy
    """
    frequency = {}  # contains all values from  from examples set + frequency
    total_freq = {}
    entropy = 0.0
    print("Length: %d" % examples.length)
    print("Target Attribute: " + target_attr)
    target_index = examples.attributes.index(target_attr)
    class_index = examples.length - 1
    print("Attribute index: %d" % target_index)
    for value in examples.values:
        if (value[target_index], value[class_index]) in frequency:
            frequency[(value[target_index], value[class_index])] += 1.0
        else:
            frequency[(value[target_index], value[class_index])] = 1.0

        if value[target_index] in total_freq:
            total_freq[value[target_index]] += 1.0
        else:
            total_freq[value[target_index]] = 1.0

    print(frequency)
    print(total_freq)
    values = list(set([x for x, y in frequency.keys()]))
    classes = list(set([y for x, y in frequency.keys()]))
    print(values)
    print(classes)
    for v in values:
        x = total_freq[v]/examples.length
        y = 0
        for cl in classes:
            if (v, cl) in frequency:
                y += (-frequency[v, cl]/examples.length) * \
                     math.log(frequency[v, cl]/examples.length, 2)
        entropy += x * y
    print("Entropy: %f" % entropy, end='\n\n')
    return entropy


def choose_attribute(examples, attributes):
    """
    Finds the attribute that best classifies examples
    :param examples:
    :param attributes:
    :return: returns the best attribute found
    """
    min_value = float("+inf")
    best_attr = None
    for attr in attributes:
        entropy_value = entropy(examples, attr)
        if entropy_value < min_value:
            min_value = entropy_value
            best_attr = attr
    return best_attr


def id3(examples, attributes, target_attr):
    if sum(x > 0 for x in examples) and not sum(x < 0 for x in examples):
        print("Positive")
    if sum(x < 0 for x in examples) and not sum(x > 0 for x in examples):
        print("Negative")

    else:
        tree = DecisionTree()
        best_attr = choose_attribute(examples, attributes)
        print(best_attr)
        tree.Node = best_attr
        # What possible values?
