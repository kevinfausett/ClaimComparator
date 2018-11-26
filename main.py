from glob import glob
from pathlib import Path
from nltk import sent_tokenize
# from ClaimComparatorModel import ClaimComparatorModel
from SentComparator.SentComparator import SentComparator
from LogicComparator.LogicComparator import LogicComparator
from scipy.stats import hmean
import os

def load():
    documents = {}
    for file in glob('./testCorpus/*.txt'):
        rawtext = Path(file).read_text()
        doc = []
        sentences = sent_tokenize(rawtext)
        for sentence in sentences:
            for segment in sentence.split('\n'):
                if segment:
                    doc.append(segment)
        documents[file] = doc
    return documents


def main():
    # documents = load()
    sc = SentComparator()
    path = "../ClaimComparator/testLogicParseCorpus/"
    files = glob(os.path.join(path, "*logic.csv"))
    # w2v = sc.loadW2V()
    for filename in files:
        with open(filename, "r", encoding='utf-8') as logic, open('results.txt', 'a', encoding='utf-8') as res:
            print('Processing:', filename)
            if 'claim 1' in filename:
               target = 'Bolsanaro won the Brazilian election'
            elif 'claim 2' in filename:
                target = 'Climate change is predominantly caused by human activity'
            else:
                target = 'Michael Jordan is the greatest basketball player of all time'
            lines = logic.readlines()
            match = sc.oneToManyCompare(lines, target)
            res.write(filename + ': ' + str(match) + '\n')

    # print(sc.compare('The sandwich ate the rat', 'The rat ate the sandwich'))
    # print(documents['./testCorpus\claim 3-7.txt'][4])
    # posCCM = ClaimComparatorModel(documents['./testCorpus\claim 3-3.txt'][-1])
    # print(posCCM.go())
    # ['[', 'russell', 'may', 'have', 'won', 'more', 'championships', ']', '[', ',', 'Chamberlain', 'may', 'have',
    #  'averaged', '50', 'points', 'per', 'game', 'in', 'a', 'single', 'season', ']', '[', 'and', 'Kareem', 'may', 'be',
    #  'the', 'all-time', 'scoring', 'leader', ']', ',', '[', 'but', 'if', '[', 'you', 'take', 'into', 'consideration',
    #  'the', 'entire', 'package', ']', ',', 'Michael', 'Jordan', 'is', 'the', 'greatest', 'of', 'all', 'time', '.', ']']

    # negCCM = ClaimComparatorModel(documents['./testCorpus\claim 3-7.txt'][4])
    # print(negCCM.go())
    # ['[', 'tonight', 'is', 'the', 'commencement', 'of', 'the', 'fourth', 'installment', 'of', 'the', 'Warriors-Cavs',
    #  'Finals', ']', ',', '[', 'which', 'resurrects', 'the', 'biggest', 'debate', 'in', 'basketball', ':', 'Is',
    #  'LeBron', 'James', 'or', 'the', 'Bulls', "'", 'Michael', 'Jordan', 'the', 'Greatest', 'Player', 'of', 'All-Time',
    #  '?', ']']

    TP, FP, FN = LogicComparator.run_on_sts()
    precision = (1.0 * TP) / (TP + FP)
    recall = (1.0 * TP) / (TP + FN)
    print("Precision: {}\nRecall: {}\nF1 Score: {}".format(precision, recall, hmean([precision, recall])))


main()

