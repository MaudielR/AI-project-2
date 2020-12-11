import copy
import math
import random
from itertools import product

print("What size board would you like?")
global W, H, M, cellSize, valid, playerPieces, agentPieces, D, select, pitLocation
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
                pitLocation.add((row,col))
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

#Returns a string of all observations. If String length == 0 then there are no observations
def Observation(node,grid,X,Y):
    observable = ""
    #Gets all cells which have an opponent piece
    observations = list(filter(lambda x: x not in node.agent and x not in pitLocation and x in node.player,scan(1,[X,Y])))
    if len(observations) >= 0:
        for obv in observations :
            r, c = obv
            nearType = grid[r][c]
            observable += nearType[1]
    return observable


def neighbors(x,y,type):
    global data_set
    #Where neighbors(x,y) are the nodes within one move of (x,y)
    problist = []
    prob = 0
    Left =0
    Right=0
    up=0
    down=0
    upLeft=0
    upRight=0
    downLeft=0
    downRight=0
    if x-1 <0:
        if y -1 < 0:
            Right= data_set[x][y+1][type]
            down = data_set[x+1][y][type]
            downRight = data_set[x+1][y+1][type]
            problist.append(Right)
            problist.append(Left)
            problist.append(downRight)
        elif y+1> D:
            Left = data_set[x][y-1][type]
            down = data_set[x+1][y][type]
            downLeft = data_set[x+1][y-1][type]
            problist.append(Left)
            problist.append(down)
            problist.append(downLeft)

        else:
            Left = data_set[x][y-1][type]
            Right = data_set[x][y+1][type]
            down = data_set[x+1][y][type]
            downLeft = data_set[x+1][y-1][type]
            downRight = data_set[x+1][y+1][type]
            problist.append(Left)
            problist.append(Right)
            problist.append(down)
            problist.append(downLeft)
            problist.append(downRight)



    if x+1 >D:
        if y-1 <0:
            Right = data_set[x][y + 1][type]
            up = data_set[x-1][y][type]
            upRight = data_set[x-1][y +1][type]
            problist.append(Right)
            problist.append(up)
            problist.append(upRight)

        elif y+1> D:
            up = data_set[x - 1][y][type]
            Left = data_set[x][y-1][type]
            upLeft = data_set[x-1][y -1][type]
            problist.append(up)
            problist.append(Left)
            problist.append(upLeft)

        else:
            Left = data_set[x][y-1][type]
            Right = data_set[x][y+1][type]
            up= data_set[x-1][y][type]
            upLeft= data_set[x-1][y-1][type]
            upRight= data_set[x-1][y+1][type]
            problist.append(Left)
            problist.append(Right)
            problist.append(up)
            problist.append(upLeft)
            problist.append(upRight)




    else:
        if y-1 < 0:

            Right = data_set[x][y+1][type]
            down = data_set[x+1][y][type]
            up = data_set[x-1][y][type]
            upRight = data_set[x-1][y+1][type]
            downRight = data_set[x+1][y+1][type]
            problist.append(Right)
            problist.append(down)
            problist.append(up)
            problist.append(upRight)
            problist.append(downRight)



        elif y+1 > D:
            Left =  data_set[x][y-1][type]
            up = data_set[x-1][y][type]
            down = data_set[x+1][y][type]
            upLeft = data_set[x-1][y-1][type]
            downLeft = data_set[x+1][y-1][type]

            problist.append(Left)
            problist.append(up)
            problist.append(down)
            problist.append(upLeft)
            problist.append(downLeft)
        else:
            up = data_set[x-1][y][type]
            down = data_set[x+1][y][type]
            Left = data_set[x][y-1][type]
            Right = data_set[x][y+1][type]
            upLeft = data_set[x-1][y-1][type]
            upRight = data_set[x-1][y+1][type]
            downLeft = data_set[x+1][y-1][type]
            downRight = data_set[x+1][y+1][type]

            problist.append(Left)
            problist.append(up)
            problist.append(down)
            problist.append(upLeft)
            problist.append(downLeft)
            problist.append(Right)
            problist.append(upRight)
            problist.append(downRight)


    c = len(problist)
    for x in problist:
        prob += (x * (1/(c*len(agentPieces))))
    return prob



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


#def Neighbors(X,Y):






def main():
    pitLocation = set()
    P_Wumpus(0, 0)
    P_Hero(0, 0)
    P_Mage(0, 0)
    grid = buildGrid(D)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))



if __name__ == '__main__':
    main()
