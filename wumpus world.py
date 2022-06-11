import random
import tkinter as tk

Agent = 1
Pit = 2
Wumpus = 3
Gold = 4
MapSize = 4

class WumpusWorldGenerator():
    def __init__(self, agent, gold):
        self.agent = agent
        self.gold = gold
        self.x_agent, self.y_agent = agent
        self.x_gold, self.y_gold = gold
        self.Indexes =[]
        self.Indexes = self.getIndexes()
        for i in range (0,3):
            rindex_x = (self.x_agent,i)
            rindex_xy = (i,self.y_agent)
            rindex_y = (i,self.y_gold)
            self.Indexes.remove(rindex_x)
            self.Indexes.remove(rindex_y)
            if rindex_xy in self.Indexes:
                self.Indexes.remove(rindex_xy)
            
        self.setAgent(self.agent)
        self.setGold(self.gold)
        self.setWumpus()
        self.setPit()
        self.block_information = {"0,0": [2, 2, 2, 2, 2, 0], "0,1": [2, 2, 2, 2, 2, 0], "0,2": [2, 2, 2, 2, 2, 0],
                                  "0,3": [2, 2, 2, 2, 2, 0],
                                  "1,0": [2, 2, 2, 2, 2, 0], "1,1": [2, 2, 2, 2, 2, 0], "1,2": [2, 2, 2, 2, 2, 0],
                                  "1,3": [2, 2, 2, 2, 2, 0],
                                  "2,0": [2, 2, 2, 2, 2, 0], "2,1": [2, 2, 2, 2, 2, 0], "2,2": [2, 2, 2, 2, 2, 0],
                                  "2,3": [2, 2, 2, 2, 2, 0],
                                  "3,0": [2, 2, 2, 2, 2, 0], "3,1": [2, 2, 2, 2, 2, 0], "3,2": [2, 2, 2, 2, 2, 0],
                                  "3,3": [2, 2, 2, 2, 2, 0]}
        self.createD()


    def format_block(self, x, y):
        return "%d,%d" % (x, y)

    def getIndexes(self):
        self.Indexes = []
        for x in range(MapSize):
            for y in range(MapSize):
                self.Indexes.append((x, y))
        return self.Indexes


    def getMatrix(item):
        matrix = []
        try:
            copy = getattr(item, 'copy')
        except AttributeError:
            copy = None
        for i in range(MapSize):
            matrix.append([])
            for j in range(MapSize):
                if copy:
                    matrix[i].append(copy())
                else:
                    matrix[i].append(item)
        return matrix


    world = getMatrix(1)

    def setElement(self, index, value):
        x, y = index
        self.world[x][y] = value 
        if index in self.Indexes:
            self.Indexes.remove(index)

    def setPit(self):
        pit_probability = [1, 1, 0, 0, 0]
        for self.index in self.Indexes:
            self.setPit = random.choice(pit_probability)
            if self.setPit:
                self.setElement(self.index, Pit)


    def setWumpus(self):
        self.index = random.choice(self.Indexes)
        self.setElement(self.index, Wumpus)


    def setGold(self, g):
        self.setElement(g, Gold)

    def setAgent(self, a):
        self.setElement(a, Agent)

    def createD(self):
        for i in range(0,4):
            for j in range(0,4):
                if self.world[i][j] == 2:
                    self.block_information[self.format_block(i, j)][0] = 1
                    self.block_information[self.format_block(i, j)][1] = 0
                    self.block_information[self.format_block(i, j)][2] = 0
                    self.block_information[self.format_block(i, j)][3] = 0
                    self.block_information[self.format_block(i, j)][4] = 0
                    temp = self.get_neighborhood(self.format_block(i,j))
                if self.world[i][j] == 3:
                    self.block_information[self.format_block(i, j)][0] = 0
                    self.block_information[self.format_block(i, j)][1] = 1
                    self.block_information[self.format_block(i, j)][2] = 0
                    self.block_information[self.format_block(i, j)][3] = 0
                    self.block_information[self.format_block(i, j)][4] = 0
                    temp = self.get_neighborhood(self.format_block(i,j))
                if self.world[i][j] == 4:
                    self.block_information[self.format_block(i, j)][0] = 0
                    self.block_information[self.format_block(i, j)][1] = 0
                    self.block_information[self.format_block(i, j)][2] = 0
                    self.block_information[self.format_block(i, j)][3] = 0
                    self.block_information[self.format_block(i, j)][4] = 1
        print(self.block_information) 

    def get_neighborhood(self, position):

        x = int(position[0])
        y = int(position[2])
        n_list = []
        x_range = x
        y_range = y

        for i in range(-1, 2, 2):
            if 3 >= x_range + i >= 0:
                n_list += [self.format_block(x + i, y)]
            if 3 >= y_range + i >= 0:
                n_list += [self.format_block(x, y + i)]
        return n_list


A = (0, 0)
G = (3, 3)
wworld = WumpusWorldGenerator(A, G)
print('Wumpus World')
mapp=wworld.world
print("""
Agent = 1
Pit = 2
Wumpus = 3
Gold = 4
""")
class Layout(tk.Tk):
    colours = ["#063a11", "#9f9363"]
    color="#563a12"
    def __init__(self, n=4):
        super().__init__()
        self.n = n
        self.leftframe = tk.Frame(self)
        self.leftframe.grid(row=0, column=0, rowspan=4, padx=10)
        self.middleframe = tk.Frame(self)
        self.middleframe.grid(row=0, column=4, rowspan=4)
        self.canvas = tk.Canvas(self, width=640, height=640)
        self.canvas.grid(row=0, column=1, columnspan=8, rowspan=8)
        self.board = [[None for row in range(n)] for col in range(n)]

    def drawboard(self,mapp):
        from itertools import cycle      
        for col in range(self.n):
            color = cycle(self.colours[::-1] if not col % 2 else self.colours)
            for row in range(self.n):
                x1 = col * 70
                y1 = (5-row) * 70
                x2 = x1 + 70
                y2 = y1 + 70
                self.board[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=next(color))              
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(mapp[col][row]), fill="White", font=('Arial 13 bold'))          
board = Layout()
board.drawboard(mapp)
board.mainloop()

