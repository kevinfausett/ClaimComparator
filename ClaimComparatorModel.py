from SyntacticParser.SyntacticParser import SyntacticParser
from LogicParser.LogicParser import LogicParser
from nltk.tokenize import sent_tokenize
from stat_parser.viterbi.viterbi_pcfg import PCFGTrainer
import csv
import glob
import os
from nltk.tree import Tree


class ClaimComparatorModel:
    def __init__(self, text, grammar=None):
        # if grammar is None:
        #     grammar = PCFGTrainer().train()
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
                    file_name = filename.lstrip(path)
                    file_name = file_name.replace("txt", "syntax")
                    save_syntactic_parse(SyntacticParser(sentence, grammar=grammar).go(False), file_name=file_name)
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


def save_logic_parse(logic_parsed, file_name="untitled_save",
                     save_path="../ClaimComparator/testLogicParseCorpus/"):
        full_file_path = save_path + file_name + ".csv"
        with open(full_file_path, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([logic_parsed])


def logic_parse_all_test_files():
    path = "../ClaimComparator/testParseTreeCorpus/"
    for filename in glob.glob(os.path.join(path, "*syntax.csv")):
            print('Processing:', filename)
            with open(filename, "r") as csvFile:
                csv_read = csv.reader(csvFile)
                for row in csv_read:
                    try:
                        answer = LogicParser(Tree.fromstring(row[0])).go_get_claims()
                    except ValueError:
                        break
                    for los in LogicParser(Tree.fromstring(row[0])).go_get_claims():
                        file_name = filename.lstrip(path)
                        file_name = file_name.replace("syntax.csv", "logic")
                        save_logic_parse(los, file_name)
                        print("saved row to:", file_name + ".csv")


# note: some parse trees were saved as invalid trees. Idk how this happened, but for now we throw them out
logic_parse_all_test_files()
