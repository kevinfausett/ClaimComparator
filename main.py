from glob import glob
from pathlib import Path
from nltk import sent_tokenize

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
    print(documents.values())

main()

