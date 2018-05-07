from math import log


def entropy(examples, attributes, target_attr):
    """
    Calculates the entropy of examples set for the target attribute.
    :param examples: examples values
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


def gain(examples, attributes, attr, target_attr):
    """
    Calculates the information gain (reduction in entropy) from the target
    attribute.
    :param examples: examples values;
    :param attributes: list of attributes;
    :param attr: chosen attribute;
    :param target_attr: target attribute;
    :return: information gain calculated.
    """
    frequency = {}
    sub_entropy = 0.0
    target_index = attributes.index(attr)

    for value in examples:
        if value[target_index] in frequency:
            frequency[value[target_index]] += 1.0
        else:
            frequency[value[target_index]] = 1.0

    for key in frequency.keys():
        prob = frequency[key] / sum(frequency.values())
        sub_examples = [value for value in examples if value[target_index] ==
                        key]
        sub_entropy += prob * entropy(sub_examples, attributes, target_attr)

    return entropy(examples, attributes, target_attr) - sub_entropy


def choose_attribute(examples, attributes, target_attr):
    """
    Finds the attribute that best classifies examples.
    :param examples: examples values;
    :param attributes: list of attributes;
    :return: returns the best attribute found.
    """
    max_gain = float("-inf")
    best_attr = attributes[0]

    for attr in attributes[1:-1]:
        gain_value = gain(examples, attributes, attr, target_attr)
        if gain_value > max_gain:
            max_gain = gain_value
            best_attr = attr
    return best_attr


def majority_value(examples, attributes, target_attr):
    """
    Returns the most common value for an attribute.
    :param examples: examples values;
    :param attributes: list of attributes;
    :param target_attr: target attribute;
    :return: the most common value for an attribute.
    """
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
    """
    Gets the values from a specific target/column.
    :param examples: examples values;
    :param attributes: list of attributes;
    :param target_attr: target attribute;
    :return: returns a list containing all values from target;
    """
    target_index = attributes.index(target_attr)
    target_values = list()
    for value in examples:
        if value[target_index] not in target_values:
            target_values.append(value[target_index])
    return target_values


def get_examples(examples, attributes, target_attr, val):
    """
    Gets the rows where the value in target attribute is val;
    :param examples: examples values;
    :param attributes: list of attributes;
    :param target_attr: target attribute;
    :param val: value to compare;
    :return: returns a new examples list.
    """
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
    Implementation of id3 algorithm.
    Based on:
    http://www.onlamp.com/pub/a/python/2006/02/09/ai_decision_trees.html
    :param examples: examples values;
    :param attributes: list of attributes;
    :param target_attr: target attribute;
    :return: returns the generated tree.
    """
    target_index = attributes.index(target_attr)
    values = [value[target_index] for value in examples]

    if not examples or (len(attributes) - 2) <= 0:
        return majority_value(examples, attributes, target_attr)
    elif values.count(values[0]) == len(values):
        return values[0]
    else:
        best_attr = choose_attribute(examples, attributes, target_attr)
        tree = {best_attr: {}}

        for value in get_values(examples, attributes, best_attr):
            new_examples = get_examples(examples, attributes, best_attr, value)

            new_attr = attributes[:]
            new_attr.remove(best_attr)

            subtree = id3(new_examples, new_attr, target_attr)

            tree[best_attr][value] = subtree

        return tree


def classify(tree, examples, attributes):
    """
    Used to classify new test examples.
    :param tree: tree generated from id3;
    :param examples: new examples values;
    :param attributes: list of attributes;
    :return: returns a list containing the class results.
    """
    class_result = list()
    for row in examples:
        result = classify_aux(tree, examples, attributes, row)
        class_result.append(result)
    return class_result


def classify_aux(tree, examples, attributes, row):
    result = ""
    while isinstance(tree, dict):
        root = next(iter(tree))
        tree = tree[root]
        index = attributes.index(root)
        value = row[index]
        if value in tree.keys():
            result = tree[value]
            tree = tree[value]
    return result
