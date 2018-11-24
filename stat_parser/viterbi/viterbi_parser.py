from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.parse import ViterbiParser
from nltk.tree import ParentedTree
from nltk import PCFG
import pickle
import re
from stat_parser.viterbi.viterbi_pcfg import PCFGTrainer

try:
    from nltk import Tree

    def nltk_tree(t):
        return Tree(t[0], [c if isinstance(c, str) else nltk_tree(c) for c in t[1:]])

    nltk_is_available = True

except ImportError:
    nltk_is_available = False

from stat_parser.tokenizer import PennTreebankTokenizer


class CustomViterbiParser:
    def __init__(self, grammar=None, load_grammar=False):
        if grammar is None:
            if load_grammar:
                file = open('./grammar.txt', 'rb')
                grammar_string = pickle.load(file)
                file.close()
                # copy the first line of the file into this lstrip method
                grammar_string = grammar_string.lstrip("Grammar with 7652 productions (start state = S)")
                print(grammar_string)
                grammar_string = re.sub(' \. ', " PERIOD ", grammar_string)
                grammar_string = re.sub(' , ', " COMMA ", grammar_string)
                grammar_string = re.sub(' -NONE- ', " NONE ", grammar_string)
                print("tried")
                self.grammar = PCFG.fromstring(grammar_string)
            else:
                pcfg_trainer = PCFGTrainer()
                self.grammar = pcfg_trainer.train()
        else:
            self.grammar = grammar
        self.unwrapped_parser = self.init_viterbi()

    # returns a viterbi parser
    def init_viterbi(self):
        return ViterbiParser(self.grammar)

    @staticmethod
    def tokenize_for_parsing(string):
        tokenizer = PennTreebankTokenizer()
        return tokenizer.tokenize(string)

    def parse(self, string):
        tokenized = word_tokenize(string)
        print(tokenized)
        tag_pairs = pos_tag(tokenized)
        tags = []
        for pair in tag_pairs:
            tags.append(pair[1])
        print(tags)
        result = None
        for tree in self.unwrapped_parser.parse(tags):
            result = tree
        if result:
            return self.pos_to_leaves(result, tokenized, tags)
        else:
            return None

    @staticmethod
    def pos_to_leaves(tree, leaves, tags):
        this_tree = ParentedTree.convert(tree=tree)
        string = ' '.join(str(this_tree).split())  # weird logic to go from tree to string
        for leaf_index in range(0, len(leaves)):
            leaf = leaves[leaf_index]
            tag = tags[leaf_index]
            old = "(" + tag + " " + tag + ")"
            new = "(" + tag + " " + leaf + ")"
            string = string.replace(old, new, 1)
        return Tree.fromstring(string)


def syntactic_parse(text, grammar=None):
    if grammar is None:
        viterbi_parser = CustomViterbiParser()
    else:
        viterbi_parser = CustomViterbiParser(grammar=grammar)
    return viterbi_parser.parse(text)


# pcfg_training = PCFGTrainer()
# grammar = pcfg_training.train()
