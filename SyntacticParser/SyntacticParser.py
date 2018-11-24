from stat_parser import Parser
from stat_parser.viterbi import viterbi_parser
from nltk.tree import Tree


class SyntacticParser:
    def __init__(self, text, grammar=None):
        self.text = text
        if grammar:
            self.grammar = grammar

    def cky_parse(self):
        parser = Parser()
        return parser.parse(self.text)

    def viterbi_parse(self):
        return viterbi_parser.syntactic_parse(self.text, grammar=self.grammar)

    def go(self, viterbi=True):
        if viterbi:
            try:
                return self.viterbi_parse()
            except ValueError:
                return Tree.fromstring("(NOT COVERED)")
        else:
            try:
                return self.cky_parse()
            except ValueError or TypeError:
                return Tree.fromstring("(NOT COVERED)")


# sp = SyntacticParser("The dog bit the man because it was angry.")
# answer = sp.go()
# answer.draw()
# print(answer)
