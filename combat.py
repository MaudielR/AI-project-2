import math
import random

from pip._vendor.distlib.compat import raw_input


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
            grid[4][row] = "AW "
            grid[D - 1][row] = "PW "
            count += 1
        elif count == 1:
            grid[4][row] = "AH "
            grid[D - 1][row] = "PH "
            count += 1
        else:
            grid[4][row] = "AM "
            grid[D - 1][row] = "PM "
            count = 0

    return grid


# Select Valid Piece, if you select an empty cell or a pit or your opponents piece it will get mad
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
        # print("The piece you have selected is: " + cur + " at the coordinates (" + str(row) + "," + str(col) + ")")
        return row, col


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
            if next[
                2] != " ":  # The user has found an opponent over a trapped space so they both die!  <This is kinda an assumption someone check up on this>
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
            grid[nR][nC] == "EE "
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


# The user who wins causes the other user to lose points
def win(user):
    global playerScore, agentScore
    if user == "P":
        agentScore -= 1
    else:
        playerScore -= 1


# Is Win but reversed
def lose(user):
    global playerScore, agentScore
    if user == "P":
        playerScore -= 1
    else:
        agentScore -= 1


# 1 is Win, -1 is Lose, 0 is Tie
def fight(user, opponent):
    if user == opponent:
        return 0
    elif user == "W":
        if opponent == "Hero":
            return 1
        else:
            return -1
    elif user == "H":
        if opponent == "Mage":
            return 1
        else:
            return -1
    else:
        if opponent == "W":
            return 1
        else:
            return -1


def isValid(index, D):
    return 0 < index < D


def distance(x1, y1, x2, y2):
    return int(math.sqrt((((x2 - x1) ** 2) + ((y2 - y1) ** 2))))


# -----------------------------------------------------------------------------------------------------------------------------------
# min max node with tsudo() code version, alphabeta(), Originial minmax()
# if it gives you erros try searching for init--funcitons--- to fix problems


class Node(object):
    def init(self, depth, alpha, beta, maximizingPlayer):
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.maximizingPlayer = maximizingPlayer
        self.childnode = []
        self.children()

    def children(self):
        if self.depth >= 0:
            # range in the next matrix postition
            for x in range(1, 8):
                v = self.beta - x
                self.children.append(Node(self.depth - 1, -self.alpha, v, self.value(v)))

    def value(self, value):
        maxsize = 10000

        if (value == 0):
            return maxsize * self.alpha
        elif (value < 0):
            return maxsize * -self.maximizingPlayer

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
        maxsize = 10000
        minsize = -10000
        if (depth == 0) or (abs(node.value()) == maxsize):
            return node.value
        if maximizingPlayer:
            Maxvalue = minsize
            prioirty_queue = []

            for child in node:
                prioirty_queue.push(child, h(child))
            while child == prioirty_queue.pop():
                value = alphabeta(self, child, depth - 1, alpha, beta, False)
                Maxvalue = max(Maxvalue, value)
                if beta <= alpha:
                    break
            return Maxvalue
        else:
            Minvalue = maxsize
            for child in node:
                prioirty_queue.push(child, -h(child))
            while child == prioirty_queue.pop():
                value = alphabeta(self, child, depth - 1, alpha, beta, True)
                Minvalue = min(Minvalue, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return Minvalue


"""
def alphabeta(node, depth,  α, β, maximizingPlayer):
        if (depth == 0) or (abs(node.value) == maxsize):
            return node.value
        if maximizingPlayer:
            Maxvalue = minsize
            prioirty_queue = []
            for child in node:
                prioirty_queue.push(child,h(child))
            while child == prioirty_queue.pop():
                value= max(value, alphabeta(child, depth − 1, α, β, FALSE))
                α= max(α, value)
                if α ≥ β:
                    break (* β cut-off *)
            return value
        else
            value= maxsize
            for child in node:
                prioirty_queue.push(child,-h(child))
            while child == prioirty_queue.pop():
                value = min(value, alphabeta(child, depth − 1, α, β, TRUE))
                β= min(β, value)
                if β ≤ α:
                    break (* α cut-off *)
            return value
# test initial call 
"""

"""
#Issues: THere is no MaxSize
#Depth is D
#Maxsize is 
#this is the plain minmax algorithm
    def minmax(node, depth, maximizingPlayer):
            if (depth == 0) or (abs(node.value) == maxsize):
                return node.value
            if maximizingPlayer:
                Maxvalue = minsize
            
                for child in node:
                    value = minmax(nide,depth -1, False)
                    Maxvalue = max(Maxvalue, value)
                return Maxvalue
            else: 
                MinValue = maxsize

                for child in node:
                    value = minmax(nide,depth -1, True)
                    Minvalue = max(Minvalue, value)
                return Minvalue

"""

def minimax(node, depth, user):
    if depth == 0 or getScore(u)


def getScore(user):
    global playerScore, agentScore
    if user == "P":
        return playerScore
    else:
        return agentScore

# ------------------------------------------------------------------------------------------------------------
def main():
    print("Input Grid Size")
    D = int(input())
    while D % 3 != 0 or D <= 0:
        print("Grid Size must be a multiple of 3 and greater than 0 ")
        D = int(input())
    print(D)
    grid = buildGrid(D)
    playerScore, agentScore = D, D

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid[4][5] = "TT "
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))


if __name__ == '__main__':
    main()
