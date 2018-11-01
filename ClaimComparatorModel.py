from SyntacticParser.SyntacticParser import SyntacticParser
from LogicParser.LogicParser import LogicParser


class ClaimComparatorModel:
    def __init__(self, text):
        self.syntax_parser = SyntacticParser(text)
        self.logic_parser = LogicParser(self.syntax_parser.go())

    def go(self):
        return self.logic_parser.go()

def demo():
    text = "Against this backdrop, a rise in violent crime has left some voters yearning for order and security, which Bolsonaro — an ex-military officer — promised to deliver. But his embrace of “law and order” carries alarming undertones, as he has expressed a fondness for the country’s past military dictatorship. His anti-democratic views are just one element of his disturbing rhetoric, though; the president-elect also freely spews misogynistic, anti-LGBTQ, and racist statements."
    ccm = ClaimComparatorModel(text)
    print(ccm.go())
