import math


class DecisionTree:
    def __init__(self, data, attributes):
        self.data = data
        self.attributes = attributes

    def entropy(self, data, target_attr):
        """
        Calculates the entropy of a data set for the target attribute.
        :param data: data set
        :param target_attr: target attribute
        :return: returns the calculated entropy
        """
        frequency = {}
        entropy = 0.0
        for record in data:
            if record[target_attr] in frequency:
                frequency[record[target_attr]] += 1.0
            else:
                frequency[record[target_attr]] = 1.0

        for freq in frequency.values():
            entropy += (-freq/len(data)) * math.log(freq/len(data), 2)

        return entropy

    def id3(sel, examples, target_attr, attributes):
