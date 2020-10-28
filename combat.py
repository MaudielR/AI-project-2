#If a piece is move into a square containing one of the opponent's
# pieces then they do battle. If a hero battles a wumpus then the her shoots the wumpus
# and kills it. If a mage does battle with a hero then it uses its fire magic to destroy the hero.
# If a wumpus does battle with a mage then the wumpus will eat the mage. If two pieces of
# the same type do battle then both pieces are destroyed.

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
            grid[1][row] = "AW "
            grid[D - 1][row] = "PW "
            count += 1
        elif count == 1:
            grid[1][row] = "AH "
            grid[D - 1][row] = "PH "
            count += 1
        else:
            grid[1][row] = "AM "
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


# If someone has fallen in a pit TT is changed to T[User who fell in] if both users have fallen in it just becomes EE
def move(cords, grid, D, user):
    print("Where would you like to move? Enter: (row,col)")
    cR, cC = cords
    nR, nC = tuple(map(int, raw_input().split(',')))
    while not (isValid(nR, D)) or not (isValid(nC, D)) or distance(nR, nC, cR, cC) != 1:
        if distance(cR, nR, cC, nC) != 1:
            print("Invalid coordinate, please input (row,col) within 1 cell of " + str(cords))
        else:
            print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + str(D))
        nR, nC = tuple(map(int, raw_input().split(',')))

    next = grid[nR][nC]
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        move(cords, grid, D, user)
    elif next[0] == "T":
        if next[1] == user:       # Someone has already fallen
            grid[nR][nC] = "T" + grid[cR][cC]
        elif next[1] != "T":      # Both have fallen in so we change to EE
            grid[nR][nC] = "EE "
        else:                     # No one has fallen
            grid[nR][nC] = "T" + user + " "
    else:
        if grid[cR][cC] == "PH" and next =="AW":
            temp = grid[cR][cC]
            grid[nR][nC] = temp[1:] + " "
        if grid[cR][cC] == "PH" and next =="AM":
            temp = next
            grid[nR][nC] = temp[1:] +" "
            
        if grid[cR][cC] == "TP" and next =="AH":
            temp = grid[cR][cC]
            grid[nR][nC] = temp[1:] + " "
        if grid[cR][cC] == "TP" and next =="AW":
            temp = next
            grid[nR][nC] = temp[1:] +" "
            
        if grid[cR][cC] == "PW" and next =="AM":
            temp = grid[cR][cC]
            grid[nR][nC] = temp[1:] + " "
        if grid[cR][cC] == "PW" and next =="AH":
            temp = next
            grid[nR][nC] = temp[1:] +" "
        if (grid[cR][cC] == "TP" and next =="AM") or (grid[cR][cC] == "PH" and next =="AH") or (grid[cR][cC] == "PW" and next =="AW"):
            next == "EE"
            grid[nR][nC] = "EE"
        if list(grid[cR][cC])[0] == "T":
            temp = grid[cR][cC]
            grid[nR][nC] = temp[1:] + " "
        else:
            grid[nR][nC] = grid[cR][cC]

        if list(grid[cR][cC])[0] == "T":
            grid[cR][cC] = "T" + user + " "
        else:
            grid[cR][cC] = "EE "
  #this will be where we will call combat 
#---------------------------------------------------
        
#---------------------------------------------------
    return grid


def isValid(index, D):
    return 0 < index < D


def distance(x1, y1, x2, y2):
    return int(math.sqrt((((x2 - x1) ** 2) + ((y2 - y1) ** 2))))

def main():
    print("Input Grid Size")
    D = int(input())
    while D % 3 != 0 or D <= 0:
        print("Grid Size must be a multiple of 3 and greater than 0 ")
        D = int(input())
    print(D)
    grid = buildGrid(D)
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
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
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