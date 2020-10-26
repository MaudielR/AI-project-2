import random

# Grid size is DxD
print("Input Grid Size")
D = int(input())
while D%3 != 0 or D<=0:
    print("Grid Size must be a multiple of 3 and greater than 0 ")
    D = int(input())
print(D)

#E is Empty and P is for Pit
grid = [["E" for i in range(D)] for j in range(D)]

for y in range(1, D-1):
    pits = (D/3)-1
    while pits != 0:
        x = random.randint(0, D-1)
        if grid[x][y] == "E":
            grid[x][y] = "P"
            pits -= 1


print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))