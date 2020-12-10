import copy
import math
import random
from itertools import product
def buildGrid(D):
    # each function will be called, TRUE OR FALSE just means if it gives off a tell that it's near

    probability = P_Pits(D) + P_Mage(0,0) + P_Hero(0,0)+P_Wumpus(0,0)
    grid = [[[probability,"EE "] for i in range(D)] for j in range(D)]

    # probability = P_Hero() + P_Mage() + P_Wumpus() + P_Pits()
    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == [P_Pits(D),"EE "]:
                grid[row][col] = "TT "
                pits -= 1

    count = 0
    for row in range(0, D):
        if count == 0:
            grid[0][row] = "AW "
            grid[0][row] = P_Wumpus(0, row)
            grid[D - 1][row] = "PW "
            grid[D - 1][row] = P_Wumpus(D - 1, row)
            count += 1
        elif count == 1:
            grid[0][row] = "AH "
            grid[0][row] = P_Hero(0, row)
            grid[D - 1][row] = "PH "
            grid[D - 1][row] = P_Hero(D - 1, row)
            count += 1
        else:
            grid[0][row] = "AM "
            grid[0][row] = P_Mage(0, row)
            grid[D - 1][row] = "PM "
            grid[D - 1][row] = P_Mage(D - 1, row)
            count = 0

    return grid



# Builds a Grid where EE is Empty and TT is for Pit, Agent occupies the top row and Player occupies the bottom row


def P_Wumpus(X, Y):

    #Before anyting Call funciton to see if there is a sing of Adjacent player

    P_Wumpus = 1
    if X == 0 and Y != 0:
        return P_Wumpus

    else:
        return 0
        # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')




def P_Hero(X, Y):
    P_Wumpus = 1
    if X == 0 and Y!=0:
        return P_Wumpus
    else:
        return 0
        # return 1 if turn 1 not in first column
        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


def P_Mage(X, Y):
    P_Wumpus = 1
    if X == 0 and Y != 0:
        return P_Wumpus

    else:
        return 0 # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


def P_Pits(D):
    P_Wumpus = 1 / 9
    return P_Wumpus
        # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')








def main():
    print("What size board would you like?")
    D = int(input())

    P_Wumpus(0, 0)
    P_Hero(0, 0)
    P_Mage(0, 0)
    grid = buildGrid(D)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))



if __name__ == '__main__':
    main()
