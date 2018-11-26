from SyntacticParser.SyntacticParser import SyntacticParser
from LogicParser.LogicParser import LogicParser
from nltk.tokenize import sent_tokenize
from stat_parser.viterbi.viterbi_pcfg import PCFGTrainer
import csv
import glob
import os
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')


class ClaimComparatorModel:
    def __init__(self, text, grammar=None):
        if grammar is None:
            grammar = PCFGTrainer().train()
        self.syntax_parser = SyntacticParser(text, grammar)
        self.logic_parser = LogicParser(self.syntax_parser.go())
        self.claims, self.parse_tree = self.logic_parser.go()


    # Compares two claims to determine if they are equivalent
    @staticmethod
    def claims_equal(c1, c2):
        subj1, verb1, obj1 = SyntacticParser.parts_of_sentence(c1)
        subj1 = preprocess_string(subj1)
        verb1 = preprocess_string(verb1)
        obj1 = preprocess_string(obj1)

        subj2, verb2, obj2 = SyntacticParser.parts_of_sentence(c2)
        subj2 = preprocess_string(subj2)
        verb2 = preprocess_string(verb2)
        obj2 = preprocess_string(obj2)

        return are_synonymous(subj1, subj2) and are_synonymous(verb1, verb2) and are_synonymous(obj1, obj2)


# Strips a leading 'the ' from the string if it exists, and replaces all spaces with underscores
def preprocess_string(string):
    if string is not None:
        if string[:4] == 'the ':
            return string[4:].replace(' ', '_')
        else:
            return string.replace(' ', '_')
    return string

# Determines if the two given phrases are synonyms
def are_synonymous(p1, p2):
    if p1 is None or p2 is None:
        return p1 is p2
    p1_set = wordnet.synsets(p1)
    p2_set = wordnet.synsets(p2)
    p1_synonyms = []
    for syn in p1_set:
        for l in syn.lemmas():
            p1_synonyms.append(l.name())
    p2_synonyms = []
    for syn in p2_set:
        for l in syn.lemmas():
            p2_synonyms.append(l.name())

    are_synonyms = False
    for sense in p1_synonyms:
        if sense in p2_synonyms:
            are_synonyms = True
    return are_synonyms

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
if __name__ == "__main__":
    text1 = "The president says the economy is improving."
    text2 = "The president claims the economy is improving."
    ccm1 = ClaimComparatorModel(text1)
    ccm2 = ClaimComparatorModel(text2)
    print(ClaimComparatorModel.claims_equal(ccm1.parse_tree, ccm2.parse_tree))
