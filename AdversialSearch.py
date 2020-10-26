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
            count == 0

    return grid


def select(grid, D, user):
    print("What piece would you like to move? Enter: (row,col)")
    row, col = tuple(map(int, raw_input().split(',')))
    while row < 0 or row >= D or col < 0 or col >= D:
        print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + D)
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
        select(grid, D, user)
    else:
        print("The piece you have selected is: " + cur + " at the coordinates (" + str(row) + "," + str(col) + ")")
        return row, col


def main():
    print("Input Grid Size")
    D = int(input())
    while D % 3 != 0 or D <= 0:
        print("Grid Size must be a multiple of 3 and greater than 0 ")
        D = int(input())
    print(D)
    grid = buildGrid(6)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))

    select(grid, D, "P")

if __name__ == '__main__':
    main()
