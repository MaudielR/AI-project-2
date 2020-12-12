import copy
import math
import pygame as p
import numpy
import random
from itertools import product
from pip._vendor.distlib.compat import raw_input

print("What size board would you like?")
global W, H, M, cellSize, valid, playerPieces, agentPieces, D, select, data_set
pitLocation = set()
width, height = 600, 600
margin = 5
valid = {}
playerPieces, agentPieces = [], []
pCord, pMove = (-1, -1), (-1, -1)



class Decision_Node:
    """A Decision Node asks a question.

    This should holds a reference to the question
    ex: [W(P), H(P), ##%, True] > 50%?
    """

    def __init__(self, question, true, false):
        self.question = question
        self.true_branch = true
        self.false_branch = false

def buildGrid(D):
    # each function will be called, TRUE OR FALSE just means if it gives off a tell that it's near
    global data_set
    data_set = [[[P_Wumpus(i,j,False), P_Mage(i,j,False), P_Hero(i,j,False), False] for i in range(D)] for j in range(D)]
    grid = [["EE " for i in range(D)] for j in range(D)]
    x = 1
    y = 1
    for row in range(1, D-1):
        for col in range(0, D):
            data_set[row][col] = ([P_Wumpus(x,y,False), P_Hero(x,y,False), P_Mage(x,y,False), False,P_Pits(D)])
            y= y+1
        x= x+1

    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE ":
                grid[row][col] = "TT "
                pits -= 1
                pitLocation.add((row, col))
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
def move(cords, grid, D, user):
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
        move(cords, grid, D, user)
    # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[:2]
            updatePosition(user,  cords, (nR, nC))
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user,  (nR, nC))
            grid[nR][nC] = "EE "
            loseAuto(user,  cords)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            loseAuto(user,  cords)
    # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
        updatePosition(user, cords, (nR, nC))
    # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            winAuto(user,  (nR, nC))
            loseAuto(user,  cords)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            winAuto(user, (nR, nC))
            updatePosition(user,  cords, (nR, nC))
        else:
            loseAuto(user,  cords)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid
# The user who wins causes the other user to lose points
def winAuto(user, cord):
    if user == "P":
        agentPieces.remove(cord)
    else:
        playerPieces.remove(cord)

# Is Win but reversed
def loseAuto(user, cord):
    if user == "P":
        playerPieces.remove(cord)
    else:
        agentPieces.remove(cord)
def updatePosition(user, cord, moveTo):
    if user == "P":
        playerPieces.remove(cord)
        playerPieces.append(moveTo)
    else:
        agentPieces.remove(cord)
        agentPieces.append(moveTo)
# Builds a Grid where EE is Empty and TT is for Pit, Agent occupies the top row and Player occupies the bottom row
def P_Hero(X, Y,bool):
    #first we need to find true false variable for observation
    #ObVi= Observation(X,Y)
    # 2 return this P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')
    global data_set
    start = gameStart()
    if not start:
        return 0
    # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')
    H = int(data_set[X][Y][0])
    neighbor = neighbors(X, Y, 1)
    Hero = 1 - (1 / D) * H + neighbor * 1 / (D * neighbor)
    return Hero

def P_Wumpus(X, Y,bool):
    global data_set
    start = gameStart()
    if not start:
        return 0
    #check if position datta_set[x][y][3] == true
    #if so MAATH
    # P'(Wx,y) = (1-1/c)*P'(Wx, y) + (x',y)(neighbors(x,y)P(Wx', y') *P(Wx,y|Wx', y')

    W = int(data_set[X][Y][0])
    neighbor= neighbors(X,Y,0)
    Wumpus = 1 -(1/D) * W + neighbor * 1/(D*neighbor)
    return Wumpus


def P_Mage(X, Y,bool):
    global data_set
    start = gameStart()
    if not start:
        return 0  # return 1 if turn 1 not in first column
    M = int(data_set[X][Y][0])
    neighbor = neighbors(X, Y, 1)
    Mage = 1 - (1 / D) * M + neighbor * 1 / (D * neighbor)
    return Mage

def P_Pits(D):
    pits = (D / 3) - 1
    if pits != 0:
        P_Wumpus = pits /((D*D)-(2*D))
        return round(P_Wumpus,2)

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


# Returns a string of all observations. If String length == 0 then there are no observations
def Observation(X,Y):
    #Gets all cells which dont have
    observations = list(filter(lambda x: x not in playerPieces,scan(1,[X,Y])))
    if len(observations) >= 0:
        for obv in observations:
            r, c = obv
            if (data_set[r][c][0] > 0):
                P_Wumpus(r,c,True)
            else: P_Wumpus(r,c,False)
            if(data_set[r][c][1] > 0):
                P_Hero(r, c, True)
            else: P_Hero(r,c,False)
            if (data_set[r][c][2] > 0):
                P_Hero(r, c, True)
            else:
                P_Hero(r, c, False)


def gameStart():
    return False
# Assume these coords are always valid
def moveAuto(cords, moveTo, grid, user):
    cR, cC = cords
    nR, nC = moveTo
    curr = grid[cR][cC]
    next = grid[nR][nC]
    # print("User: " + user + " Cords: " + str(cords) + " moveTo: " + str(moveTo))
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[:2]
            updatePosition(user, cords, moveTo)
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user,  moveTo)
            grid[nR][nC] = "EE "
            loseAuto(user,  cords)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            loseAuto(user, cords)
        # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
        updatePosition(user,  cords, moveTo)
        # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            winAuto(user,  moveTo)
            loseAuto(user,  cords)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            winAuto(user,  moveTo)
            updatePosition(user,cords, moveTo)
        else:
            loseAuto(user,  cords)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid
def neighborsSet(D, cell):
    n = []
    for x in product(*(range(coords - 1, coords + 2) for coords in cell)):
        if x != cell and all(0 <= n < D for n in x):
            n.append(x)
    return n
def evaluatePosition( gird):
    evaluation = 0
    for piece in agentPieces:
        pR, pC = piece
        pieceType = gird[pR][pC]
        if pieceType[0] == "T":
            pT = pieceType[2]
        else:
            pT = pieceType[1]
        # Every player piece near agent piece
        for nearPlayer in list(filter(lambda x: x not in agentPieces and x in playerPieces,neighborSetScalable(D,piece))):
            nR, nC = nearPlayer
            nearType = gird[nR][nC]
            if nearType[0] == "T":
                nT = nearType[2]
            else:
                nT = nearType[1]
            evaluation += fight(pT, nT)
    return evaluation + ((len(agentPieces) - len(playerPieces))*1.5)
def neighborSetScalable(D, cell):
    n = []
    for x in product(*(range(coords - (D//3), coords + 1 + (D//3)) for coords in cell)):
        if x != cell and all(0 <= n < D for n in x):
            n.append(x)
    return n


def setGlobals(IO):
    global W, H, M, cellSize, valid, playerPieces, agentPieces, D
    D = IO
    while D%3 != 0:
        print("Size of the board must be a multiple of 3")
        D = int(input())
    cellSize = (width // D) - margin
    W = p.transform.scale(p.image.load("Wumpus.png"), (cellSize, cellSize))
    H = p.transform.scale(p.image.load("Hero.png"), (cellSize, cellSize))
    M = p.transform.scale(p.image.load("Mage.png"), (cellSize, cellSize))
    for x in range(0, D):
        for y in range(0, D):
            valid[(x, y)] = neighborsSet(D, (x, y))
    for i in range(0, D):
        playerPieces.append((D - 1, i))
        agentPieces.append((0, i))


def main():

    setGlobals(int(input()))
    grid = buildGrid(D)
    gameStart()
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in data_set]))
    p.init()
    clock = p.time.Clock()
    screen = p.display.set_mode((width + 100, height))
    screen.fill(p.Color("black"))
    running = True

    AI = 0
    font = p.font.SysFont('Calibri', 35);
    On = font.render('On', True, p.Color("Black"))
    Off = font.render('Off', True, p.Color("Black"));
    fog = False
    #Build_Decision_Tree(data_set,1)
    while running:
        p.draw.rect(screen, p.Color("Green"), [610, 50, 80, 40])
        p.draw.rect(screen, p.Color("Red"), [610, 150, 80, 40])
        screen.blit(On, (630, 55))
        screen.blit(Off, (630, 155))
        if len(playerPieces) == 0 or len(agentPieces) == 0:
            break
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if pos[0] > 400:
                    if pos[1] >= 50 and pos[1] <= 90:
                        print("On")
                        fog = True
                    if pos[1] >= 150 and pos[1] <= 190:
                        print("Off")
                        fog = False
                elif AI == 0:
                    choosen = random.randint(0, len(agentPieces)-1)
                    nC, nR = agentPieces[choosen]
                    Observation(nC, nR)
                    print("Starting MinMax Algo")
                    moves = list(filter(lambda x: x not in agentPieces,scan(1,(nC,nR))))
                    moveTo = moves[random.randint(0,len(moves)-1)]
                    moveAuto((nC, nR), moveTo, grid, "A")
                    AI += 1
                else:
                    print("You may now select a piece")
                    pC = pos[0] // (cellSize + margin)
                    pR = pos[1] // (cellSize + margin)

                    if AI == 1:
                        cur = grid[pR][pC]
                        if cur[0] != "P":
                            if cur[0] == "E":
                                print("This is an empty cell")
                            elif cur[0] == "T":
                                if cur[1] == "P" and cur[2] != " ":
                                    print("You have selected a piece!")
                                    pCord = (pR, pC)
                                    AI += 1
                                else:
                                    print("This is a pit")
                            else:
                                print("You have selected your opponents piece")
                        else:
                            print("You have selected a piece!")
                            pCord = (pR, pC)
                            AI += 1
                    elif (pR, pC) in list(filter(lambda x: x not in playerPieces, valid[pCord])):
                        pMove = (pR, pC)
                        moveAuto(pCord, pMove, grid, "P")
                        AI = 0
                    else:
                        print("This is an invalid piece")
        clock.tick(15)
        screen = drawBoard(screen, grid, fog,data_set)
        p.display.flip()
    if len(playerPieces) == 0 and len(agentPieces) == 0:
        print("TIE!")
    elif len(agentPieces) == 0:
        print("Player Won!")
    else:
        print("Player Lost!")
    p.quit
# Draw board state
def drawBoard(screen, grid, fog, probability):
    font = p.font.SysFont('Calibri', 20);
    for r in range(D):
        for c in range(D):
            type = grid[r][c]
            if type[0] != "T":
                if type[0] != "P" and fog:
                    p.draw.rect(screen, p.Color("Grey"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize,
                                 cellSize])

                else:
                    p.draw.rect(screen, p.Color("White"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize])
                    loadPiece(screen, type[1], r, c)
            else:
                if type[1] == "P":
                    p.draw.rect(screen, p.Color("Green"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize,
                                 cellSize])
                elif type[1] == "A":
                    p.draw.rect(screen, p.Color("Red"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize,
                                 cellSize])
                else:
                    p.draw.rect(screen, p.Color("Grey"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize])
                loadPiece(screen, type[2], r, c)
            prob = str(probability[r][c][0]) + "," + str(probability[r][c][1]) + "," + str(probability[r][c][2])
            num = font.render(prob, True, p.Color("Red"))
            screen.blit(num, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize,
                                    cellSize))
    return screen

def loadPiece(screen, type, r, c):
    if type == "W":
        screen.blit(W, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize))
    elif type == "H":
        screen.blit(H, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize))
    elif type == "M":
        screen.blit(M, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize))


if __name__ == '__main__':
    main()
