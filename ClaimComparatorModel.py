from SyntacticParser.SyntacticParser import SyntacticParser
from LogicParser.LogicParser import LogicParser
from nltk.tokenize import sent_tokenize
from stat_parser.viterbi.viterbi_pcfg import PCFGTrainer
import csv
import glob
import os


class ClaimComparatorModel:
    def __init__(self, text, grammar=None):
        if grammar is None:
            grammar = PCFGTrainer().train()
        self.syntax_parser = SyntacticParser(text, grammar)
        self.logic_parser = LogicParser(self.syntax_parser.go())

    def go(self):
        return self.logic_parser.go()


def demo(text_here, grammar=None):
    results = []
    for sentence in sent_tokenize(text_here):
        a_ccm = ClaimComparatorModel(sentence, grammar=grammar)
        result = a_ccm.go()
        results.append(result)
        print(result)
    return results


def save_syntactic_parse(parse_tree, file_name="untitled_save",
                         save_path="../ClaimComparator/testParseTreeCorpus/"):
        full_file_path = save_path + file_name + ".csv"
        with open(full_file_path, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            print(parse_tree)
            writer.writerow([parse_tree])


def syntactic_parse_all_test_files(grammar=PCFGTrainer().train()):
    path = "../ClaimComparator/testCorpus/"
    for filename in glob.glob(os.path.join(path, "*.txt")):
            print('Processing:', filename)
            with open(filename, "r", encoding="ISO-8859-1") as textFile:
                file_as_string = ""
                for line in textFile:
                    file_as_string = file_as_string + line
                for sentence in sent_tokenize(file_as_string):
                    file_name = filename.lstrip("../ClaimComparator/testCorpus/")
                    file_name = file_name.replace("txt", "syntax")
                    save_syntactic_parse(SyntacticParser(sentence, grammar=grammar).go(False), file_name=file_name)


# text = "Against this backdrop, a rise in violent crime has left some voters yearning for order and security, which Bolsonaro — an ex-military officer — promised to deliver. But his embrace of “law and order” carries alarming undertones, as he has expressed a fondness for the country’s past military dictatorship. His anti-democratic views are just one element of his disturbing rhetoric, though; the president-elect also freely spews misogynistic, anti-LGBTQ, and racist statements."
# demo(text, grammar=PCFGTrainer().train())
syntactic_parse_all_test_files()
