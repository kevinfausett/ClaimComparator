from nltk import Nonterminal
from nltk import induce_pcfg
from nltk import ViterbiParser
from nltk.tree import ParentedTree
from nltk.tree import Tree
import glob
import os
import re
import pickle


class PCFGTrainer:
    def __init__(self, proportion_train_trees=None):
        if proportion_train_trees is None:
            self.prop_train = 0.9  # DEFAULT
        else:
            self.prop_train = proportion_train_trees
        self.tree_corpus = []  # a list of solved trees for training and testing
        self.tree_corpus_pos_leaves = []  # a list of solved trees for training and testing with pos for leaves
        self.productions = []  # a list of productions derived from train_trees
        self.train_trees = []  # a list of the training trees pulled from tree_corpus
        self.test_trees = []   # a list of the testing trees pulled from tree_corpus
        self.trained_grammar = None
        self.load_trees()
        self.leaves_to_pos()
        self.set_train_test_trees(self.prop_train)
        self.set_productions()

    # load the file as a list of tokens
    def load_trees(self):
        path = "../treebanks/PennTreebank"
        dirname = os.path.dirname(__file__)
        dirpath = os.path.join(dirname, path)
        for filename in glob.glob(os.path.join(dirpath, "*.mrg")):
            print('Processing:', filename)
            with open(filename, "r", encoding="ISO-8859-1") as textFiles:
                trees = []
                this_tree = ""
                paren_count = 0
                for line in textFiles.readlines():
                    if line is "\n":
                        continue
                    # in tree
                    open_paren = len(re.findall("\(", line))
                    close_paren = len(re.findall("\)", line))
                    paren_count = paren_count + open_paren - close_paren
                    for string in line.split():
                        this_tree = this_tree + " " + string
                        # end of tree
                    if paren_count == 0:
                        this_tree = self.delete_outer_parens(this_tree)
                        tree = Tree.fromstring(this_tree)
                        # tree.chomsky_normal_form()
                        trees.append(tree)
                        this_tree = ""
                self.tree_corpus = self.tree_corpus + trees

    @staticmethod
    def delete_outer_parens(string):
        first_paren_index = 0
        last_parent_index = 0
        for index in range(0, len(string)):
            if string[index] == "(":
                first_paren_index = index
                break
        for index in range(first_paren_index, len(string)):
            if string[index] == ")":
                last_parent_index = index
        return string[first_paren_index + 1:last_parent_index]

    # set_train_test_trees: sets the fields train_trees and test_trees according to the given proportion
    def set_train_test_trees(self, prop_train, from_tokens=False):
        if 0 < prop_train < 1:
            if from_tokens:
                number_train = int(prop_train * len(self.tree_corpus))
                self.train_trees = self.tree_corpus[:number_train]
                self.test_trees = self.tree_corpus[number_train:]
            else:
                number_train = int(prop_train * len(self.tree_corpus_pos_leaves))
                self.train_trees = self.tree_corpus_pos_leaves[:number_train]
                self.test_trees = self.tree_corpus_pos_leaves[number_train:]
        else:
            print("InputError: the given proportion is not between 0 and 1!")

    # set_productions: sets the field productions with the productions derived from the training trees
    def set_productions(self):
        self.productions = []
        for tree in self.train_trees:
            for production in tree.productions():
                self.productions.append(production)

    # returns the grammar trained by this trainer
    def train(self):
        if self.trained_grammar is None:
            s = Nonterminal('S')
            self.trained_grammar = induce_pcfg(s, self.productions)
        return self.trained_grammar

    # evaluate: returns the proportion of test_trees properly constructed by the grammar
    # that was trained by this trainer using train_trees
    # TODO: condense for loops
    def evaluate(self, print_tree_mismatch=False):
        # First, flatten the answer key
        test_pos_list = []
        for test_tree in self.test_trees:
            test_pos_list.append(test_tree.leaves())
        # Second, get the grammar
        if self.trained_grammar is None:
            self.trained_grammar = self.train()
        # Third, build trees back up with your grammar
        trees_built_by_grammar = []
        for pos_list in test_pos_list:
            print(pos_list)
            syntactic_parsed_result = self.syntactic_parse(pos_list, self.trained_grammar)
            print("done parsing")
            if syntactic_parsed_result is not None:
                print(syntactic_parsed_result)
                trees_built_by_grammar.append(Tree.convert(syntactic_parsed_result))
            else:
                print(syntactic_parsed_result)
                trees_built_by_grammar.append(Tree.fromstring("(NOT COVERED)"))
        # Finally, get a proportion of correct trees
        number_correct = 0
        number_trees = len(trees_built_by_grammar)
        for index in range(number_trees):
            print(index)
            if self.test_trees[index] == trees_built_by_grammar[index]:
                number_correct += 1
            elif print_tree_mismatch:
                print("\nTREE MISMATCH", "\nConstructed:\n",
                      trees_built_by_grammar[index], "\nOriginal:\n", self.test_trees[index])
        return number_correct / number_trees

    # returns None if it cannot make the tree
    @staticmethod
    def syntactic_parse(pos_list, grammar):
        parser = ViterbiParser(grammar)
        try:
            grammar.check_coverage(pos_list)
        except ValueError:
            return None
        for tree in parser.parse(pos_list):
            return tree

    def leaves_to_pos(self):
        for tree in self.tree_corpus:
            this_tree = ParentedTree.convert(tree=tree)
            leaves = this_tree.leaves()
            pos_tags = this_tree.pos()
            string = ' '.join(str(this_tree).split())  # weird logic to go from tree to string
            for leaf_index in range(0, len(leaves)):
                leaf = leaves[leaf_index]
                tag = pos_tags[leaf_index][1]
                string = string.replace(leaf, tag, 1)
            self.tree_corpus_pos_leaves.append(Tree.fromstring(string))

    def dump_grammar(self):
        file = open("./grammar.txt", 'wb')
        pickle.dump(str(self.train()), file)
        file.close()


# pcfg_train = PCFGTrainer()
# pcfg_train.dump_grammar()
# print(pcfg_train.tree_corpus_pos_leaves)
# pcfg_train.train()
# print(pcfg_train.trained_grammar)
# print(pcfg_train.evaluate(True))
