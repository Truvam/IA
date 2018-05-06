from math import log


def entropy(examples, attributes, target_attr):
    """
    Calculates the entropy of examples set for the target attribute.
    :param examples: examples set
    :param target_attr: target attribute
    :return: returns the calculated entropy
    """
    frequency = {}  # contains all values from  from examples + frequency
    total_freq = {}
    entropy = 0.0
    target_index = attributes.index(target_attr)
    class_index = -1

    for value in examples:
        if (value[target_index], value[class_index]) in frequency:
            frequency[(value[target_index], value[class_index])] += 1.0
        else:
            frequency[(value[target_index], value[class_index])] = 1.0

        if value[target_index] in total_freq:
            total_freq[value[target_index]] += 1.0
        else:
            total_freq[value[target_index]] = 1.0

    values = list(set([x for x, y in frequency.keys()]))
    classes = list(set([y for x, y in frequency.keys()]))

    for v in values:
        x = total_freq[v]/len(examples)
        y = 0.0
        for cl in classes:
            if (v, cl) in frequency:
                y += (-frequency[v, cl]/len(examples)) * \
                     log(frequency[v, cl]/len(examples), 2)
        entropy += x * y

    return entropy


def choose_attribute(examples, attributes):
    """
    Finds the attribute that best classifies examples.
    :param examples: examples values;
    :param attributes: list of attributes from csv file;
    :return: returns the best attribute found.
    """
    min_value = float("+inf")
    best_attr = None
    for attr in attributes[1:-1]:
        entropy_value = entropy(examples, attributes, attr)
        if entropy_value < min_value:
            min_value = entropy_value
            best_attr = attr
    return best_attr


def majority_value(examples, attributes, target_attr):
    frequency = {}
    target_index = attributes.index(target_attr)
    for value in examples:
        if value[target_index] in frequency:
            frequency[value[target_index]] += 1
        else:
            frequency[value[target_index]] = 1

    max_value = float("-inf")
    val = ""
    for key in frequency.keys():
        if frequency[key] > max_value:
            max_value = frequency[key]
            val = key
    return val


def get_values(examples, attributes, target_attr):
    target_index = attributes.index(target_attr)
    target_values = list()
    for value in examples:
        if value[target_index] not in target_values:
            target_values.append(value[target_index])
    return target_values


def get_examples(examples, attributes, target_attr, val):
    target_index = attributes.index(target_attr)
    new_examples = list(list())
    for value in examples:
        if value[target_index] == val:
            new_value = list()
            for i in range(0, len(value)):
                if i != target_index:
                    new_value.append(value[i])
            new_examples.append(new_value)
    return new_examples


def id3(examples, attributes, target_attr):
    """
    Based on:
    http://www.onlamp.com/pub/a/python/2006/02/09/ai_decision_trees.html

    """

    target_index = attributes.index(target_attr)
    values = [value[target_index] for value in examples]

    if not examples or (len(attributes) - 2) <= 0:
        return majority_value(examples, attributes, target_attr)
    elif values.count(values[0]) == len(values):
        return values[0]
    else:
        best_attr = choose_attribute(examples, attributes)
        tree = {best_attr: {}}

        for value in get_values(examples, attributes, best_attr):
            new_examples = get_examples(examples, attributes, best_attr, value)

            new_attr = attributes[:]
            new_attr.remove(best_attr)

            subtree = id3(new_examples, new_attr, target_attr)

            tree[best_attr][value] = subtree

        return tree
