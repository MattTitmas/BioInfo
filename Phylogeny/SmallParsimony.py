import math
from functools import lru_cache
from typing import Dict

from Helpful_Structures import BinaryTree


# Implementation of the Small Parsimony Algorithm


class ParsimonyTree(BinaryTree):
    def __init__(self, value):
        super().__init__(value)
        self.minimums = None

    def add_left_child(self, child):
        if type(child) == 'ParsimonyTree':
            self.left = child
        else:
            self.left = ParsimonyTree(child)

    def add_right_child(self, child):
        if type(child) == 'ParsimonyTree':
            self.right = child
        else:
            self.right = ParsimonyTree(child)

    def backtrack(self, smallest_value_previous, character, previous_choice=None):
        if previous_choice is None:
            self.left.backtrack(smallest_value_previous, character, '')
            self.right.backtrack(smallest_value_previous, character, '')
            return

        if self.left is None and self.right is None:
            return

        minimum_score = min([i for i in self.minimums.values()])
        if self.minimums[smallest_value_previous] == minimum_score:
            self.value += smallest_value_previous
            self.left.backtrack(smallest_value_previous, character, '')
            self.right.backtrack(smallest_value_previous, character, '')
        else:
            smallest_value = min(self.minimums, key=self.minimums.get)
            self.value += smallest_value
            self.left.backtrack(smallest_value, character, '')
            self.right.backtrack(smallest_value, character, '')

    def __small_parsimony_inner(self, character: int):
        if self.left is None and self.right is None:
            values = {k: 0 if k == self.value[character] == k else float('inf') for k in ['A', 'C', 'G', 'T']}
            self.minimums = values
            return values
        to_return_dict = dict()
        small_parsimony_left = self.left.__small_parsimony_inner(character)
        small_parsimony_right = self.right.__small_parsimony_inner(character)
        for k in ['A', 'C', 'G', 'T']:
            min_one, min_two = [], []
            for i in ['A', 'C', 'G', 'T']:
                min_one.append(small_parsimony_left[i] + delta(i, k))
                min_two.append(small_parsimony_right[i] + delta(i, k))
            to_return_dict[k] = min(min_one) + min(min_two)
        self.minimums = to_return_dict
        return to_return_dict

    def small_parsimony(self):
        stored = self.left
        while stored.left is not None:
            stored = stored.left
        length = len(stored.value)

        new_value = ""
        for i in range(0, length):
            dictionary = self.__small_parsimony_inner(i)
            smallest_value = min(dictionary, key=dictionary.get)
            self.backtrack(smallest_value, i)
            new_value += smallest_value
        self.value = new_value

    def parsimony_score(self):
        if self.minimums is None:
            return -1
        if self.left is None and self.right is None:
            return 0
        left_difference = sum(1 for a, b in zip(self.left.value, self.value) if a != b)
        right_difference = sum(1 for a, b in zip(self.right.value, self.value) if a != b)
        return left_difference + right_difference + self.left.parsimony_score() + self.right.parsimony_score()

def delta(i, k):
    return 0 if i == k else 1


def main():
    parsimony_tree = ParsimonyTree('')
    parsimony_tree.add_left_child('')
    parsimony_tree.left.add_left_child('ACGTAGGCCT')
    parsimony_tree.left.add_right_child('ATGTAAGACT')
    parsimony_tree.add_right_child('')
    parsimony_tree.right.add_left_child('TCGAGAGCAC')
    parsimony_tree.right.add_right_child('TCGAAAGCAT')

    # perform small parsimony on the tree, changing the value of all nodes to the optimal value
    parsimony_tree.small_parsimony()

    print(parsimony_tree)
    print(parsimony_tree.parsimony_score())


if __name__ == '__main__':
    main()
