from stat_parser import Parser
from stat_parser.viterbi import viterbi_parser


class SyntacticParser:
    def __init__(self, text):
        self.text = text

    def cky_parse(self):
        parser = Parser()
        return parser.parse(self.text)

    def viterbi_parse(self):
        return viterbi_parser.syntactic_parse(self.text)

    def go(self, viterbi=True):
        if viterbi:
            return self.viterbi_parse()
        else:
            return self.cky_parse()


# sp = SyntacticParser("The dog bit the man because it was angry.")
# answer = sp.go()
# answer.draw()
# print(answer)
