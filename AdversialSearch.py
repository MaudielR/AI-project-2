import math
import random

from pip._vendor.distlib.compat import raw_input


def buildGrid(D):
    # Grid size is DxD
    # EE is Empty and TT is for Pit
    grid = [["EE" for i in range(D)] for j in range(D)]

    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE":
                grid[row][col] = "TT"
                pits -= 1

    count = 0;
    for row in range(0, D):
        if count == 0:
            grid[0][row] = "AW"
            grid[D - 1][row] = "PW"
            count += 1
        elif count == 1:
            grid[0][row] = "AH"
            grid[D - 1][row] = "PH"
            count += 1
        else:
            grid[0][row] = "AM"
            grid[D - 1][row] = "PM"
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
    if cur[0] != user:
        print(cur)
        if cur[0] == "E":
            print("This is an empty cell")
        elif cur[0] == "T":
            print("This is a pit")
        else:
            print("You have selected your opponents piece")
        selectValid(grid, D, user)
    else:
        print("The piece you have selected is: " + cur + " at the coordinates (" + str(row) + "," + str(col) + ")")
        return row, col


def move(cords, grid, D, user):
    print("Where would you like to move? Enter: (row,col)")
    cR, cC = cords
    nR, nC = tuple(map(int, raw_input().split(',')))
    while not (isValid(nR, D)) or not (isValid(nC, D)) or distance(cR, nR, cC, nC) != 1:
        if distance(cR, nR, cC, nC) != 1:
            print("Invalid coordinate, please input (row,col) within 1 cell of " + str(cords))
        else:
            print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + str(D))
        nR, nC = tuple(map(int, raw_input().split(',')))
    next = grid[nR][nC]
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        move(cords, grid, D, user)
    else:
        #If it's TT we would just delete it here and not replace, and if it's the opponent we will create a seperate method for that
        grid[nR][nC] = grid[cR][cC]
        grid[cR][cC] = "EE"
        return grid


def isValid(index, D):
    return 0 < index < D


def distance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def main():
    print("Input Grid Size")
    D = int(input())
    while D % 3 != 0 or D <= 0:
        print("Grid Size must be a multiple of 3 and greater than 0 ")
        D = int(input())
    print(D)
    grid = buildGrid(6)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))


if __name__ == '__main__':
    main()
