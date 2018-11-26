from SyntacticParser.SyntacticParser import SyntacticParser
import nltk
from nltk.corpus import wordnet
from nltk.tree import Tree

nltk.download('wordnet')


class LogicComparator:
    def __init__(self):
        print('Initializing logical comparator...')

    # Compares two claims to determine if they are equivalent
    @staticmethod
    def claims_equal(c1, c2):
        sent_parts = SyntacticParser.parts_of_sentence(c1)
        if sent_parts is None:
            return False
        subj1, verb1, obj1 = sent_parts
        subj1 = preprocess_string(subj1)
        verb1 = preprocess_string(verb1)
        obj1 = preprocess_string(obj1)

        sent_parts = SyntacticParser.parts_of_sentence(c2)
        if sent_parts is None:
            return False
        subj2, verb2, obj2 = sent_parts
        subj2 = preprocess_string(subj2)
        verb2 = preprocess_string(verb2)
        obj2 = preprocess_string(obj2)

        return are_synonymous(subj1, subj2) and are_synonymous(verb1, verb2) and are_synonymous(obj1, obj2)

    # Runs the comparator on our sts test set
    @staticmethod
    def run_on_sts():
        sents_1_trees = []
        sents_2_trees = []
        labels = []

        file = open('stsParsedSent1.csv', 'r')
        sents_text = file.read()
        file.close()
        trees_1 = sents_text.split('\n\n')
        file = open('stsParsedSent2.csv', 'r')
        sents_text = file.read()
        file.close()
        trees_2 = sents_text.split('\n\n')
        file = open('stsParsedLabels', 'r')
        labels_text = file.read()
        file.close()
        labels_list = labels_text.split('\n')

        for i in range(len(trees_1)):
            sent_1 = trees_1[i]
            sent_2 = trees_2[i]
            if (sent_1 != '' and sent_2 != '') and (sent_1 != '(NOT COVERED)' and sent_2 != '(NOT COVERED)'):
                sent_1_tree = Tree.fromstring(sent_1)
                sent_2_tree = Tree.fromstring(sent_2)
                sents_1_trees.append(sent_1_tree)
                sents_2_trees.append(sent_2_tree)
                labels.append(labels_list[i])

        if len(sents_1_trees) != len(sents_2_trees):
            raise ValueError("Unequal number of sentences: {} vs {}".format(len(sents_1_trees), len(sents_2_trees)))

        TP = 0
        FP = 0
        FN = 0
        for i in range(len(sents_1_trees)):
            sent_1 = sents_1_trees[i]
            sent_2 = sents_2_trees[i]
            if sent_1 != '(NOT COVERED)' and sent_2 != '(NOT COVERED)':
                label = labels[i]

                predicted_result = LogicComparator.claims_equal(sent_1, sent_2)
                predicted_label = '1' if predicted_result else '0'

                if predicted_label == '1' and label == '1':
                    TP += 1
                elif predicted_label == '1' and label == '0':
                    FP += 1
                elif predicted_label == '0' and label == '1':
                    FN += 1

        return TP, FP, FN


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
        return False
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
