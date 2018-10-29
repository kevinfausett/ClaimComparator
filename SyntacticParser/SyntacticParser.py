from stat_parser import Parser


class SyntacticParser:
    def __init__(self, text):
        self.text = text

    def syntactic_parse(self):
        parser = Parser()
        return parser.parse(self.text)

    def go(self):
        return self.syntactic_parse()


# sp = SyntacticParser("The dog bit the man because it was angry.")
# answer = sp.go()
# answer.draw()
# print(answer)
