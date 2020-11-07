import math
import sys
from itertools import product
from pip._vendor.distlib.compat import raw_input
import random
import tkinter as tk
from PIL import ImageTK, Image

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=540, height=540, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 9
        self.columns = 9
        self.cellwidth = 60
        self.cellheight = 60
        self.W = ImageTK.PhotoImage(Image.open("Wumpus.png"))
        self.H = ImageTK.PhotoImage(Image.open("Hero.png"))
        self.M = ImageTK.PhotoImage(Image.open("Mage.png"))
        self.rect = {}
        self.oval = {}
        for column in range(9):
            for row in range(9):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
                
                #self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")

        
if __name__ == "__main__":
    app = App()
    app.mainloop()


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
#root = Tk()
#topFrame = Frame(root)
#topFrame.pack()
#bottomFrame = Frame(root)
#bottomFrame.pack(side = BOTTOM)

#button = Button(topFrame, text = "button 1")
#theLabel = Label(root, text ="Label")
#theLabel.pack()



#frame = Frame(root, width =600, height=500)
#frame.pack()






    

#def main():
    








#if __name__ == '__main__':
    #main()