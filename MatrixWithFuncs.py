import copy
import math
import numpy
import random
from itertools import product
from pip._vendor.distlib.compat import raw_input
print("What size board would you like?")
global W, H, M, cellSize, valid, playerPieces, agentPieces, D, select
data_set = []
D = int(input())

class Node(object):
    # Maximizing player is true if Agent, False if User
    # userPieces and opponentPieces is a list of all pieces
    def __init__(self, AI_Player, agentPieces, playerPieces):
        self.AI_Player = AI_Player
        self.agent = agentPieces
        self.player = playerPieces


def buildGrid(D):
    # each function will be called, TRUE OR FALSE just means if it gives off a tell that it's near
    M = 0
    H=0
    W= P_Wumpus(0,0)
    P = P_Pits(D)

    grid = [["EE " for i in range(D)] for j in range(D)]
    x = 0
    y = 0
    for row in grid:
        for col in row:
            data_set.append([ P_Pits(D),P_Wumpus(x,y), P_Hero(x,y), P_Mage(x,y)])
            y= y+1
        x= x+1
    print("THIS IS DATA SET ______")
    print(data_set)
    print(" ______")
    # probability = P_Hero() + P_Mage() + P_Wumpus() + P_Pits()
    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE ":
                grid[row][col] = "TT "
                pits -= 1

    count = 0
    for row in range(0, D):
        if count == 0:
            grid[0][row] = "AW "
            grid[D - 1][row] = "PW "
            count += 1
        elif count == 1:
            grid[0][row] = "AH "
            grid[D - 1][row] = "PH "
            count += 1
        else:
            grid[0][row] = "AM "
            grid[D - 1][row] = "PM "
            count = 0

    return grid

def selectValid(grid, D, user):
    print("What piece would you like to move? Enter: (row,col)")
    row, col = tuple(map(int, raw_input().split(',')))
    while not isValid(row, D) or not (isValid(col, D)):
        print(grid[row][col])
        print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + str(D))
        row, col = tuple(map(int, raw_input().split(',')))

    cur = grid[row][col]
    if cur[0] != user and cur[1] != user:
        print(cur)
        if cur[0] == "E":
            print("This is an empty cell")
        elif cur[1] == "T":
            print("This is a pit")
        else:
            print("You have selected your opponents piece")
        selectValid(grid, D, user)
    else:
        print("The piece you have selected is: " + cur + " at the coordinates (" + str(row) + "," + str(col) + ")")
        return row, col
# 1 is Win, -1 is Lose, 0 is Tie
def fight(user, opponent):
    if user == opponent:
        return 0
    elif user == "W":
        if opponent == "M":
            return 1
        else:
            return -1
    elif user == "H":
        if opponent == "W":
            return 1
        else:
            return -1
    else:
        if opponent == "H":
            return 1
        else:
            return -1
def isValid(index, D):
    return 0 <= index < D

def distance(x1, y1, x2, y2):
    return int(math.sqrt((((x2 - x1) ** 2) + ((y2 - y1) ** 2))))

# If someone has fallen in a pit TT is changed to T[User who fell in] if both users have fallen in it just becomes EE
def move(cords, grid, D, user, node):
    print("Where would you like to move? Enter: (row,col)")
    cR, cC = cords
    nR, nC = tuple(map(int, raw_input().split(',')))
    curr = grid[cR][cC]
    while not (isValid(nR, D)) or not (isValid(nC, D)) or distance(nR, nC, cR, cC) != 1:
        if distance(cR, nR, cC, nC) != 1:
            print("Invalid coordinate, please input (row,col) within 1 cell of " + str(cords))
        else:
            print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + str(D))
        nR, nC = tuple(map(int, raw_input().split(',')))

    next = grid[nR][nC]

    # Decides what happens to the targeted cell
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        move(cords, grid, D, user, node)
    # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[:2]
            updatePosition(user, node, cords, (nR, nC))
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user, node, (nR, nC))
            grid[nR][nC] = "EE "
            loseAuto(user, node, cords)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            loseAuto(user, node, cords)
    # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
        updatePosition(user, node, cords, (nR, nC))
    # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            winAuto(user, node, (nR, nC))
            loseAuto(user, node, cords)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            winAuto(user, node, (nR, nC))
            updatePosition(user, node, cords, (nR, nC))
        else:
            loseAuto(user, node, cords)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid
# The user who wins causes the other user to lose points
def winAuto(user, node, cord):
    if user == "P":
        node.agent.remove(cord)
    else:
        node.player.remove(cord)


# Is Win but reversed
def loseAuto(user, node, cord):
    if user == "P":
        node.player.remove(cord)
    else:
        node.agent.remove(cord)
def updatePosition(user, node, cord, moveTo):
    if user == "P":
        node.player.remove(cord)
        node.player.append(moveTo)
    else:
        node.agent.remove(cord)
        node.agent.append(moveTo)
# Builds a Grid where EE is Empty and TT is for Pit, Agent occupies the top row and Player occupies the bottom row

def neighbors(x,y):
    return


def P_Wumpus(X, Y):

    #Before anyting Call funciton to see if there is a sing of Adjacent player

    P_Wum = 1
    if X == 0 and Y == 0:
        return True

    else:
        return 2
        # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')






def P_Hero(X, Y):
        #first we need to find true false variable for observation
        #ObVi= Observation(X,Y)
        # 2 return this P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')
        P_Wumpus = 1

        if X == 0 and Y == 1:
            return True

        else:
            return 2



def P_Mage(X, Y):
    P_Wumpus = 1
    if X == 0 and Y == 2:
        return True

    else:
        return 2 # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


def P_Pits(D):
    P_Wumpus = 1 / D
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





def main():

    P_Wumpus(0, 0)
    P_Hero(0, 0)
    P_Mage(0, 0)
    grid = buildGrid(D)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print(data_set)


if __name__ == '__main__':
    main()
