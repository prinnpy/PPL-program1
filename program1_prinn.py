"""
Name: Prinn Prinyanut
Class: CSCI 3415
Due: 06/26/19
"""

from __future__ import print_function
import os
import re
import sys


def isnonterminal(x_var):
    """" return nonterminal """
    return isinstance(x_var, str) and re.match(r"^<.*>$", x_var) is not None


def isterminal(x_var):
    """" return terminal """
    return isinstance(x_var, str) and not isnonterminal(x_var)


def begin_item(grammar):
    """ return the start symbol in the grammar """
    return grammar[0][0]


def read_grammar(filepath):
    """ read in grammar function and return the entire grammar """
    grammar = []
    current_lhs = None

    def make_rule(lhs, rhs):
        """ make rule func and return lhs and rhs """
        if not isnonterminal(lhs):
            raise Exception("LHS {} is not a nonterminal".format(lhs))
        if not rhs:
            raise Exception("Empty RHS")
        return (lhs, rhs)

    def parse_rhs(lexemes):
        """ parse rhs """
        rules = []
        rhs = []
        for lex in lexemes:
            if lex == "|":
                rules.append(make_rule(current_lhs, rhs))
                rhs = []
            else:
                rhs.append(lex)
        rules.append(make_rule(current_lhs, rhs))
        return rules

    with open(filepath) as file_p:
        for line in file_p:
            lexemes = line.split()
            if not lexemes:
                pass
            elif len(lexemes) == 1:
                raise Exception("Illegal rule {}".format(line))
            elif isnonterminal(lexemes[0]) and lexemes[1] == "->":
                current_lhs = lexemes[0]
                grammar.extend(parse_rhs(lexemes[2:]))
            elif lexemes[0] == "|":
                grammar.extend(parse_rhs(lexemes[1:]))
            else:
                raise Exception("Illegal rule {}".format(line))

    return grammar


def left_derivation(grammar, form, sentence):
    """ func that return the correct left derivation """

    def correct_rule(grammar, nonterminal):
        """ return found item """
        # return list(filter(lambda rule: rule[0] == nonterminal, grammar))
        return list([rule for rule in grammar if rule[0] == nonterminal])

    def match_equation(form, sentence):
        """ match_equation derivation to the given equation """
        for i, lex in enumerate(form):
            if i == len(sentence):
                return -1
            if isnonterminal(lex):
                return i
            if lex != sentence[i]:
                return -1
        return len(sentence) if len(sentence) == len(form) else -1

    def replace(rule, form, match):
        """ get the latest matched list """
        return form[:match] + rule[1] + form[match + 1:]

    is_match = match_equation(form, sentence)
    if is_match == -1:
        return None
    if is_match == len(sentence):
        return []
    for rule in correct_rule(grammar, form[is_match]):
        correct_form = replace(rule, form, is_match)
        if len(correct_form) <= len(sentence):
            derivation = left_derivation(grammar, correct_form, sentence)
            if derivation is not None:
                return [correct_form] + derivation

    return None


def print_grammar(grammar):
    """ print entire grammar """
    for rule in grammar:
        print("{} -> {}".format(rule[0], " ".join(rule[1])))


def print_derive(grammar, derivation):
    """ print derivation grammar """

    start = begin_item(grammar)
    blank = " " * len(start)
    print("Derivation:")
    if derivation is None:
        print("Not derivation found")
    else:
        for i, form in enumerate(derivation, 1):
            print("{:4d}: {} -> {}".format(i, start if i == 1 else blank, " ".join(form)))


def main():
    """ main program """
    filepath = sys.argv[1]
    # filepath = "example_3.4.txt" #hard code text file

    if not os.path.isfile(filepath):
        raise Exception("File path {} does not exist.".format(filepath))

    print("Reading grammar from {}".format(filepath))
    grammar = read_grammar(filepath)
    print_grammar(grammar)

    while True:
        print("---")
        equation = input("Enter a sentence: \n").split() #get input and split into array
        start = [begin_item(grammar)] #get the first form Ex: ['<program>']
        result = left_derivation(grammar, start, equation) #get the result

        #print results
        print("Sentence:")
        print(" ".join(equation))
        print_derive(grammar, result)


if __name__ == "__main__":
    main()
