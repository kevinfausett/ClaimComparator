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
            except TypeError:
                return Tree.fromstring("(NOT COVERED)")
            except ValueError:
                return Tree.fromstring("(NOT COVERED)")

    # The subject of a sentence is defined as the first NP that is a child of an S and sibling of a VP
    # The object of a sentence is defined as the first NP that is a child of a VP
    # Returns the subject, main verb, and direct object of the sentence as strings, or None if it can't find that element
    @staticmethod
    def parts_of_sentence(parse_tree):
        if parse_tree.label()[0] == 'S' or '+S' in parse_tree.label():
            if parse_tree[0].label()[0] == 'S' or '+S' in parse_tree[0].label() and parse_tree[1].label() == '.':
                return SyntacticParser.parts_of_sentence(parse_tree[0])
            subject = None
            sibling_VP = False
            verb = None
            object = None
            for phrase in parse_tree:
                if phrase.label() == 'NP' and subject is None:
                    subject = ' '.join(phrase.leaves())
                elif phrase.label() == 'VP':
                    sibling_VP = True
                    for subphrase in phrase:
                        if 'VB' in subphrase.label():
                            verb = ' '.join(subphrase.leaves())
                        elif subphrase.label() == 'NP':
                            object = ' '.join(subphrase.leaves())
            if not sibling_VP:
                subject = None
            return subject, verb, object
        else:
            for phrase in parse_tree:
                if phrase.label()[0] == 'S' or '+S' in parse_tree.label():
                    return SyntacticParser.parts_of_sentence(phrase)


# sp = SyntacticParser("The dog bit the man because it was angry.")
# answer = sp.go()
# answer.draw()
# print(answer)
