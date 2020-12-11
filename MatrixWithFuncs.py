import copy
import math
import numpy
import random
from itertools import product
from pip._vendor.distlib.compat import raw_input
print("What size board would you like?")
global W, H, M, cellSize, valid, playerPieces, agentPieces, D, select, data_set
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
    global data_set
    data_set = [[[P_Wumpus(i,j), P_Mage(i,j), P_Hero(i,j)] for i in range(D)] for j in range(D)]
    grid = [["EE " for i in range(D)] for j in range(D)]
    x = 1
    y = 1
    for row in range(1, D-1):
        for col in range(0, D):
            data_set[row][col] = ([P_Wumpus(x,y), P_Hero(x,y), P_Mage(x,y), P_Pits(D)])
            y= y+1
        x= x+1

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
            data_set[0][row][0]=1
            grid[D - 1][row] = "PW "
            data_set[D-1][row][0] = 1
            count += 1
        elif count == 1:
            grid[0][row] = "AH "
            data_set[0][row][1] = 1
            grid[D - 1][row] = "PH "
            data_set[D - 1][row][1] = 1
            count += 1
        else:
            grid[0][row] = "AM "
            data_set[0][row][2] =1
            grid[D - 1][row] = "PM "
            data_set[D - 1][row][2] = 1
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
    global data_set
    start = gameStart()

    while start:
        return 0

    #Before anyting Call funciton to see if there is a sing of Adjacent player


        # return 1 if turn 1 not in first column

    W = int(data_set[X][Y][0])
    Wumpus = 1 -(1/D) * W + 1/(D + )
        # Prime_of_W =
        # P_Wum = 1/D * data_set[X][Y][1]
        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')






def P_Hero(X, Y):
        #first we need to find true false variable for observation
        #ObVi= Observation(X,Y)
        # 2 return this P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')
        global data_set
        start = gameStart()
        if not start:
            return 0



def P_Mage(X, Y):
    global data_set
    start = gameStart()
    if not start:
        return 0  # return 1 if turn 1 not in first column

        # return 0 if turn 1 and not in first row

        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')


def P_Pits(D):
    pits = (D / 3) - 1
    if pits != 0:
        P_Wumpus = pits /((D*D)-(2*D))
        return round(P_Wumpus,2)



        # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')

#Scans a radius around the cell. Radius of 1 is 3x3, radius of 2 is 5x5
def scan(radius, cell):
    n = []
    for x in product(*(range(coords - radius, coords + 1 + radius) for coords in cell)):
        if x != cell and all(0 <= n < (radius*3) for n in x):
            n.append(x)
    return n

def neighbors(x,y,type):
    global data_set
    #Where neighbors(x,y) are the nodes within one move of (x,y)
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
            left=0
            right= data_set[x][y+1][type]
            down = data_set[x+1][y][type]
            downLeft = 0
            downRight = data_set[x+1][y+1][type]
        elif y+1> D:
            right = 0
            left = data_set[x][y-1][type]
            down = data_set[x+1][y][type]
            downLeft = data_set[x+1][y-1][type]
            downRight = 0
        else:
            Left = data_set[x][y-1][type]
            Right = data_set[x][y+1][type]
            down = data_set[x+1][y][type]
            downLeft = data_set[x+1][y-1][type]
            downRight = data_set[x+1][y+1][type]

    if x+1 >D:

        if y-1 <0:
            left = 0
            right = data_set[x][y + 1][type]
            up=data_set[x-1][y][type]
            down = 0
            upLeft = 0
            upRight = data_set[x-1][y +1][type]
        elif y+1> 0:
            right = 0
            up = data_set[x - 1][y][type]
            left = data_set[x][y-1][type]
            upLeft = data_set[x-1][y -1][type]
            upRight = 0
        else:
            Left = data_set[x][y-1][type]
            Right = data_set[x][y+1][type]
            up= data_set[x-1][y][type]
            upLeft= data_set[x-1][y-1][type]
            upRight= data_set[x-1][y+1][type]
        return

    for data_set[x][y] in range(x+1,y):
    return data_set[][][0]


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


def gameStart():
    return False


def main():

    P_Wumpus(0, 0)
    P_Hero(0, 0)
    P_Mage(0, 0)
    grid = buildGrid(D)

    gameStart()
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in data_set]))

if __name__ == '__main__':
    main()
