#!/usr/bin/env python3


from nltk import parse
import re


def load_sentences(sentence=None, file=None):
    if file is not None:
        file = open(file, "r")
        for line in file:
            if "%" not in line:
                sent = re.search("(?<=sentence\(X, \[).*[a-zA-Z]", line)
                if sent is not None:
                    sent = sent.group().split(",")
                    sent[0] = sent[0].replace("'", "")
                    sent = " ".join(sent)
                    print("Sentence: " + sent)
                    analyze_sentence(sent)
    else:
        analyze_sentence(sentence)


def analyze_sentence(sentence):
    # http://www.nltk.org/book/ch09.html#code-feat0cfg
    cp = parse.load_parser('grammar.fcfg', trace=0)
    tokens = sentence.split()
    found = False
    try:
        for tree in cp.parse(tokens):
            print(tree)
            found = True
    except ValueError as e:
        print(e)
    if not found:
        print("False.")
    else:
        print()


def main():
    print("Portuguese Grammar:")
    op = input("Do you want to load test_sentences.pl? [y/n]: ")
    if op == "y" or op == "yes":
        load_sentences(file="test_sentences.pl")
    else:
        print("Write your sentence (Example: A menina corre para a floresta):")
        sentence = input("Sentence: ")
        load_sentences(sentence=sentence)


if __name__ == "__main__":
    main()
