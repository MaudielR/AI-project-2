import numpy as np
import pandas as pd



# Function importing Dataset

def buildGridTree(D):
    x = 1/21
    grid = [[x for i in range(D)] for j in range(D)]

    count = 0
    for row in range(0, D):
        if count == 0:
            grid[0][row] = 1
            grid[D - 1][row] = 0
            count += 1
        elif count == 1:
            grid[0][row] = 1
            grid[D - 1][row] = 0
            count += 1
        else:
            grid[0][row] = 1
            grid[D - 1][row] = 0
            count = 0

    return grid


# Function to split the dataset
def splitdataset(balance_data):


    return balance_data




# Function to perform training with entropy.
#def entropy(X_train, X_test, y_train):
    # Decision tree with entropy
 #    entropy = Build_Decision_Tree(S,Attributes = )

    # Performing training
  #   entropy.fit(X_train, y_train)
   # return entropy


class Information_Gain(State, attribute):
#    entropy(State)
    pass

#Decision Tree
# S = turns taken? or set of Elements not sure
#not sure What attributes are or how to define them
def Build_Decision_Tree(S, Attributes):
    if S == 'Turn 0 ':
        return
    else:
        BestGain =Information_Gain(S,A)
        BestGain = -1;
        for a in Attributes:
            S_prime = S/a;
            if Information_Gain(S_prime,A) > Information_Gain(S,A):
                IGbest = IGbest(S)
                a_best = a
        S_prime = S/a
        for all in S_prime:
            Build_Decision_Tree(S_prime,Attributes/a_best)





def main():
    # Building Phase
    grid = buildGridTree(9)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))






# Calling main function
if __name__ == "__main__":
    main()