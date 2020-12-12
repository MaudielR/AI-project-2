import random

import numpy as np
import pandas as pd

# global data set contains values of Player1, AI, Weighted_values, True false narratives based on pieces and values
# ex: player Wampus 'PW' -> AI wumpus 'AW' kille each other = 0 gain, negative outcome = FALSE


# this return the value sets of columns such as player columns or Weighted values, or Boolean outcomes
# ex data_set_values(data_set, 3) will return all true false values for each column
def data_set_values(rows, columns):
    values = set([row[columns] for row in rows])
    return values


class Leaf:
    """A Leaf node classifies data.

    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    """A Decision Node asks a question.

    This should holds a reference to the question
    ex: [W(P), H(P), ##%, True] > 50%?
    """

    def __init__(self, question, true, false):
        self.question = question
        self.true_branch = true
        self.false_branch = false


# Function importing Dataset
class Question:
    """A Question is used to partition a dataset.

    This class just records a 'column number' (e.g., 0 for Color) and a
    'column value' (e.g., Green). The 'match' method is used to compare
    the feature value in an example to the feature value stored in the
    question. See the demo below.
    """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value



def partition(rows, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    Question should be an AI decision ex: should I move W(x,y) to x+1,y?
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows





def class_counts(grid):
    """Counts the number of each type of example in a dataset."""
    counts = {"AW", "AH", "AW"}  # a dictionary of label -> count. P =pits
    for row in grid:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def gini(grid):
    """
    This should return the differences of pieces on the board, 1/9
    """
    counts = class_counts(grid)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(grid))
        impurity -= prob_of_lbl ** 2
    return impurity




# Function to perform training with entropy.
# def entropy(X_train, X_test, y_train):
# Decision tree with entropy
#    entropy = Build_Decision_Tree(S,Attributes = )

# Performing training
#   entropy.fit(X_train, y_train)
# return entropy



def find_best_split(grid):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_probability_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(grid)
    n_features = len(grid[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature

        values = set([row[col] for row in grid])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partition(grid, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain > best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


# Decision Tree
# S = turns taken? or set of Elements not sure
# not sure What attributes are or how to define them




