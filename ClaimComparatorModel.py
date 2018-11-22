from SyntacticParser.SyntacticParser import SyntacticParser
from LogicParser.LogicParser import LogicParser
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')


class ClaimComparatorModel:
    def __init__(self, text):
        self.syntax_parser = SyntacticParser(text)
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
    if string[:4] == 'the ':
        return string[4:].replace(' ', '_')
    else:
        return string.replace(' ', '_')


# Determines if the two given phrases are synonyms
def are_synonymous(p1, p2):
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


if __name__ == "__main__":
    text = "The president won the election."
    ccm = ClaimComparatorModel(text)
    print(ClaimComparatorModel.claims_equal(ccm.parse_tree, ccm.parse_tree))
