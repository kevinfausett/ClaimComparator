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
    f = open('sts-test.csv', encoding='utf-8')
    lines = f.readlines()
    labels, sent1, sent2 = [], [], []

    for i in range(len(lines)):
        splitline = lines[i].split('\t')
        score = float(splitline[4])
        s1 = splitline[5]
        s2 = splitline[6]

        if score >= 4.6:
            val = '1'
        else:
            val = '0'
        labels.append(val)
        sent1.append(s1)
        sent2.append(s2)


    l = open('stsParsedLabels', 'a')
    for i in range(len(sent1)):
        l.write(labels[i])
        l.write('\n')
        save_syntactic_parse(SyntacticParser(sent1[i], grammar=grammar).go(False), file_name='stsParsedSent1')
        save_syntactic_parse(SyntacticParser(sent2[i], grammar=grammar).go(False), file_name='stsParsedSent2')

# text = "Against this backdrop, a rise in violent crime has left some voters yearning for order and security, which Bolsonaro — an ex-military officer — promised to deliver. But his embrace of “law and order” carries alarming undertones, as he has expressed a fondness for the country’s past military dictatorship. His anti-democratic views are just one element of his disturbing rhetoric, though; the president-elect also freely spews misogynistic, anti-LGBTQ, and racist statements."
# demo(text, grammar=PCFGTrainer().train())
syntactic_parse_all_test_files()
# 2.5, 3.1, 3.6, 3.7, 3.9, 3.10, and 3.13 failed
