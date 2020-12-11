import copy
import math
import random
from itertools import product

print("What size board would you like?")
global W, H, M, cellSize, valid, playerPieces, agentPieces, D, select
D = int(input())

class Node(object):
    # Maximizing player is true if Agent, False if User
    # userPieces and opponentPieces is a list of all pieces
    def __init__(self, maximizingPlayer, agentPieces, playerPieces):
        self.maximizingPlayer = maximizingPlayer
        self.agent = agentPieces
        self.player = playerPieces


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
    ObVi = Observation(X, Y)
    P_Wumpus = 1
    if X == 0 and Y == 0:
        return 0

    else:

        return P_Wumpus
        # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


#Scans a radius around the cell. Radius of 1 is 3x3, radius of 2 is 5x5
def scan(radius, cell):
    n = []
    for x in product(*(range(coords - radius, coords + 1 + radius) for coords in cell)):
        if x != cell and all(0 <= n < (radius*3) for n in x):
            n.append(x)
    return n


def Observation(node,grid,X,Y):
    observations = {}
    playerArea = scan(1,[X,Y])
    #Get all Agents Near Player
    for nearPlayer in list(filter(lambda x: x not in node.agent and x in node.player,scan(2,[X,Y]))):
        nR, nC = nearPlayer
        nearType = grid[nR][nC]
        enemyArea = scan(3,[X,Y])
        #All cells where the player can observe
        observable = filter(lambda x: x not in playerArea,enemyArea)
        for cell in observable:
            #If this doesn't work add a if(not in)
            observations[cell] += nearType[1]
    return observations



def evaluatePosition(node, gird):
    evaluation = 0
    for piece in node.agent:
        pR, pC = piece
        pieceType = gird[pR][pC]
        if pieceType[0] == "T":
            pT = pieceType[2]
        else:
            pT = pieceType[1]
        # Every player piece near agent piece
        for nearPlayer in list(filter(lambda x: x not in node.agent and x in node.player,neighborSetScalable(D,piece))):
            nR, nC = nearPlayer
            nearType = gird[nR][nC]
            if nearType[0] == "T":
                nT = nearType[2]
            else:
                nT = nearType[1]
            evaluation += fight(pT, nT)
    return evaluation + ((len(node.agent) - len(node.player))*1.5)


def neighbors(x,y):
    return


def P_Hero(X, Y):
        #first we need to find true false variable for observation
        ObVi= Observation(X,Y)
        probability = 0
        # 2 return this P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')
        P_Wumpus = 1
        if X == 0 and Y == 0:
            return 0
        else:
            P_Wumpus = (1 - (1 / len(agentPieces)))*P_Wumpus + Neighbors(X, Y)
            return P_Wumpus



def P_Mage(X, Y):
    P_Wumpus = 1
    if X == 0 and Y == 0:
        return 0

    else:
        return P_Wumpus # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


def P_Pits(D):
    P_Wumpus = 1 / 9
    return P_Wumpus
        # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


def Neighbors(X,Y):






def main():

    P_Wumpus(0, 0)
    P_Hero(0, 0)
    P_Mage(0, 0)
    grid = buildGrid(D)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))



if __name__ == '__main__':
    main()
