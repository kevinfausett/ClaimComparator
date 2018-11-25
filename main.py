from glob import glob
from pathlib import Path
from nltk import sent_tokenize
# from ClaimComparatorModel import ClaimComparatorModel
from SentComparator.SentComparator import SentComparator

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
    documents = load()
    sc = SentComparator()
    # sc.FindCutoff()
    # sc.getPearson()
    sc.getPrecisionAndRecall()


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


main()

