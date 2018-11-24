from nltk.tree import ParentedTree
from SyntacticParser.SyntacticParser import SyntacticParser


# This class represents a logic parser.
# A logic parser parses out the smallest units of logic (logical propositions)
# from a syntax tree. There are _ criteria for a phrase to qualify as a LS phrase...
class LogicParser:
    def __init__(self, parse_tree):
        print("init")
        self.parse_tree = ParentedTree.convert(tree=parse_tree)
        self.left_bracket_indices = []
        self.right_bracket_indices = []
        self.dominant_nodes = ["S"]
        self.set_indices()
        self.result = self.parse_tree.leaves()

    # set_indices: sets the left_bracket_indices and right_bracket_indices parameters
    def set_indices(self):
        print("set_indices")
        for subtree in self.parse_tree.subtrees():
            if self.is_logic_unit(subtree):
                absolute_tp_left_edge = subtree.treeposition() + \
                                        subtree.leaf_treeposition(0)
                absolute_tp_right_edge = subtree.treeposition() + \
                    subtree.leaf_treeposition(len(subtree.leaves()) - 1)
                self.left_bracket_indices.append(
                    self.index_from_tp(absolute_tp_left_edge))
                self.right_bracket_indices.append(
                    self.index_from_tp(absolute_tp_right_edge))
        self.left_bracket_indices.sort(reverse=True)
        self.right_bracket_indices.sort(reverse=True)

    # index_from_tp: returns the index of the leaf given its tree position
    # returns nothing if there is no such leaf
    def index_from_tp(self, tree_position):
        for index in range(len(self.tp_list())):
            if self.tp_list()[index] == tree_position:
                return index

    # tp_list: returns
    def tp_list(self):
        return [self.parse_tree.leaf_treeposition(i)
                for i in range(len(self.parse_tree.leaves()))]

    # is_logic_unit: returns a boolean which is true if the given tree is an ls unit
    def is_logic_unit(self, tree):
        criterion1 = tree.label() in self.dominant_nodes
        if tree.parent():
            pass  # TODO: more criteria
        print("is logic unit")
        return criterion1

    # insert_delimiters: inserts brackets arounds
    def insert_delimiters(self):
        lefts = self.left_bracket_indices
        rights = self.right_bracket_indices
        while lefts and rights:
            if lefts[0] > rights[0]:
                self.result.insert(lefts.pop(0), "[")
            else:
                self.result.insert(rights.pop(0) + 1, "]")
        while lefts:
                self.result.insert(lefts.pop(0), "[")
        while rights:
                self.result.insert(rights.pop(0) + 1, "]")

    # go: converts parse_tree into pos with ls delimiters
    def go(self):
        self.insert_delimiters()
        return self.result


# text = "Against this backdrop, a rise in violent crime has left some voters yearning for order and security, which Bolsonaro — an ex-military officer — promised to deliver. But his embrace of “law and order” carries alarming undertones, as he has expressed a fondness for the country’s past military dictatorship. His anti-democratic views are just one element of his disturbing rhetoric, though; the president-elect also freely spews misogynistic, anti-LGBTQ, and racist statements."
# text = "The dog is lost because it does not have a collar."
# lp = LogicParser(SyntacticParser(text).go())
# lp.parse_tree.draw()
# print(lp.parse_tree)
# print(lp.dominant_nodes)
# print(lp.go())
