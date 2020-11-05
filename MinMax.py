import math
import random
import sys
from itertools import product
import copy

from pip._vendor.distlib.compat import raw_input


class Node(object):
    # Maximizing player should be a boolean
    # userPieces and opponentPieces is a list of all pieces
    # Child is currently up for debate so ignore
    # We can treat node value as len of lists, though it doesn't exists
    # Also I'm ignoring alpha and beta for now lol
    def __init__(self, maximizingPlayer, agentPieces, playerPieces):
        self.maximizingPlayer = maximizingPlayer
        # self.value = initalScore
        self.agent = agentPieces
        self.player = playerPieces


def buildGrid(D):
    # Grid size is DxD
    # EE is Empty and TT is for Pit
    grid = [["EE " for i in range(D)] for j in range(D)]

    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE ":
                grid[row][col] = "TT "
                pits -= 1

    count = 0;
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


# Select Valid Coordinates
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


"""
# If someone has fallen in a pit TT is changed to T[User who fell in] if both users have fallen in it just becomes EE
def move(cords, grid, D, user):
    global playerScore, agentScore
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
            grid[nR][nC] = "T" + curr[0, 1]
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                win(user)
            grid[nR][nC] = "EE "
            lose(user)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            lose(user)
    # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
    # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            win(user)
            lose(user)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            win(user)
        else:
            lose(user)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid
"""


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


def neighborsSet(D, cell):
    n = []
    for x in product(*(range(coords - 1, coords + 2) for coords in cell)):
        if x != cell and all(0 <= n < D for n in x):
            n.append(x)
    return n


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


# Assume these coords are always valid
def moveAuto(cords, moveTo, grid, user, node):
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
            updatePosition(user, node, cords, moveTo)
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user, node, moveTo)
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
        updatePosition(user, node, cords, moveTo)
        # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            winAuto(user, node, moveTo)
            loseAuto(user, node, cords)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            winAuto(user, node, moveTo)
            updatePosition(user, node, cords, moveTo)
        else:
            loseAuto(user, node, cords)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid


# Select Valid Coordinates
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


# Assume maximizing player is always Agent for the sake of simplicity
# maximizingPlayer just needs to a boolean in this case, if user true, if not false
def NoPruningMinmax(node, depth, grid):
    global valid
    # print("Depth " +str(depth))
    if depth == 0 or (len(node.agent) == 0 or len(node.player) == 0):
        # print("Returning Now " + str(len(node.agent)-len(node.player)))
        return evaluatePosition(node, grid), depth
    if node.maximizingPlayer:
        maxVal = -10000000
        bestMove, origin = None, None
        # Look at every piece the current user possesses
        for piece in node.agent:
            # Filter Valid Coordinates by List of User Pieces
            for validMove in list(filter(lambda x: x not in node.agent, valid[piece])):
                #print("MAX Piece :" + str(piece) + " validMove: " + str(validMove))
                tempGrid = copy.deepcopy(grid)  # Shallow copy of the Grid so as not to effect the actual game
                next = Node(False, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                # Here we updated user and opponent lists within the next node on the temporary grid
                moveAuto(piece, validMove, tempGrid, "A", next)
                # Now we get the Max, we stay on the temporary grid cause algorithm isn't finished
                val = minmax(next, depth - 1, tempGrid)[0]
                #print("maxVal: " + str(maxVal) + " Val: " + str(val))
                maxVal = max(maxVal, val)
                alpha = max(alpha, maxVal)
                if maxVal == val:
                    origin = piece
                    bestMove = validMove

        return maxVal, origin, bestMove
    else:
        minVal = 100000000
        bestMove, origin = None, None
        for piece in node.player:
            for validMove in list(filter(lambda x: x not in node.player, valid[piece])):
                #print("MIN Piece :" + str(piece) + " validMove: " + str(validMove))
                tempGrid = copy.deepcopy(grid)
                next = Node(True, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                moveAuto(piece, validMove, tempGrid, "P", next)
                val = minmax(next, depth - 1, tempGrid)[0]
                #print("minVal: " + str(minVal) + " Val: " + str(val))
                minVal = min(minVal, val)
                beta = min(beta, minVal)
                if minVal == val:
                    origin = piece
                    bestMove = validMove
        return minVal, origin, bestMove


# Assume maximizing player is always Agent for the sake of simplicity
# maximizingPlayer just needs to a boolean in this case, if user true, if not false
def minmax(node, depth, grid, alpha, beta):
    global valid
    # print("Depth " +str(depth))
    if depth == 0 or (len(node.agent) == 0 or len(node.player) == 0):
        # print("Returning Now " + str(len(node.agent)-len(node.player)))
        return evaluatePosition(node, grid), depth
    if node.maximizingPlayer:
        maxVal = -10000000
        bestMove, origin = None, None
        # Look at every piece the current user possesses
        for piece in node.agent:
            # Filter Valid Coordinates by List of User Pieces
            for validMove in list(filter(lambda x: x not in node.agent, valid[piece])):
                """if piece == (0,1) and validMove == (1,1):
                    print("Here")"""
                #print("MAX Piece :" + str(piece) + " validMove: " + str(validMove))
                tempGrid = copy.deepcopy(grid)  # Shallow copy of the Grid so as not to effect the actual game
                next = Node(False, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                # Here we updated user and opponent lists within the next node on the temporary grid
                moveAuto(piece, validMove, tempGrid, "A", next)
                # Now we get the Max, we stay on the temporary grid cause algorithm isn't finished
                val = minmax(next, depth - 1, tempGrid, alpha, beta)[0]
                #print("maxVal: " + str(maxVal) + " Val: " + str(val))
                maxVal = max(maxVal, val)
                alpha = max(alpha, maxVal)
                if maxVal == val:
                    origin = piece
                    bestMove = validMove
                if beta <= alpha:
                    break
        return maxVal, origin, bestMove
    else:
        minVal = 100000000
        bestMove, origin = None, None
        for piece in node.player:
            for validMove in list(filter(lambda x: x not in node.player, valid[piece])):
                #print("MIN Piece :" + str(piece) + " validMove: " + str(validMove))
                tempGrid = copy.deepcopy(grid)
                next = Node(True, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                moveAuto(piece, validMove, tempGrid, "P", next)
                val = minmax(next, depth - 1, tempGrid, alpha, beta)[0]
                #print("minVal: " + str(minVal) + " Val: " + str(val))
                minVal = min(minVal, val)
                beta = min(beta, minVal)
                if minVal == val:
                    origin = piece
                    bestMove = validMove
                if beta <= alpha:
                    break
        return minVal, origin, bestMove

def getChild(nodeList):
    global valid
    children = []
    for piece in nodeList:
        # Filter Valid Coordinates by List of User Pieces
        for validMove in list(filter(lambda x: x not in nodeList, valid[piece])):
            children.append((piece,validMove))
    return children


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
        for nearPlayer in list(filter(lambda x: x not in node.agent and x in node.player, valid[piece])):
            nR, nC = nearPlayer
            nearType = gird[nR][nC]
            if nearType[0] == "T":
                nT = nearType[2]
            else:
                nT = nearType[1]
            evaluation += fight(pT, nT)
    return evaluation + (len(node.agent) - len(node.player))


def main():
    global valid
    print("What size board would you like?")
    D = int(input())
    playerPieces, agentPieces = [], []
    for i in range(0, D):
        playerPieces.append((D - 1, i))
        agentPieces.append((0, i))

    valid = {}
    for x in range(0, D):
        for y in range(0, D):
            valid[(x, y)] = neighborsSet(D, (x, y))
    grid = buildGrid(D)
    # print(valid)
    node = Node(True, agentPieces, playerPieces)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    """
    This is for manual evaluation testing
    grid[0][1] = "EE "
    grid[1][1] = "AH "
    updatePosition("A", node, (0, 1), (1, 1))
    print("Updated")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print(evaluatePosition(node,grid))"""
    while len(node.player)!= 0 and len(node.agent) != 0:
        print("Starting MinMax Algo")
        first, cord, moveTo = minmax(node, 4, grid, -100000, 1000000)
        print(first)
        moveAuto(cord, moveTo, grid, "A", node)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
        if len(node.player) == 0 or len(node.agent) == 0:
            break
        cords = selectValid(grid, D, "P")
        move(cords, grid, D, "P", node)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))

    """ print("Starting MinMax Algo")
    first, cord, moveTo = minmax(0, node, D, grid)
    moveAuto(cord, moveTo, grid, "A", node)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    """


if __name__ == '__main__':
    main()
