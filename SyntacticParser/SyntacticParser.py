from stat_parser import Parser


class SyntacticParser:
    def __init__(self, text):
        self.text = text

    def syntactic_parse(self):
        parser = Parser()
        return parser.parse(self.text)

    # The subject of a sentence is defined as the first NP that is a child of an S and sibling of a VP
    # The object of a sentence is defined as the first NP that is a child of a VP
    # Returns the subject, main verb, and direct object of the sentence as strings, or None if it can't find that element
    @staticmethod
    def parts_of_sentence(parse_tree):
        if parse_tree.label()[0] == 'S':
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
                if phrase.label()[0] == 'S':
                    return SyntacticParser.parts_of_sentence(phrase)

    def go(self):
        return self.syntactic_parse()


# sp = SyntacticParser("The dog bit the man because it was angry.")
# answer = sp.go()
# answer.draw()
# print(answer)
