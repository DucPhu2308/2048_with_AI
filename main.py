#2048 Game with AI
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
from collections import deque
from PIL import Image, ImageTk
import time
from tile import Tile
class Gameplay:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.title("2048")

        self.step = 0
        self.state = np.zeros((4, 4), dtype=np.int32)
        self.initializeComponents()
        self.addNewTile()
        self.root.bind("<Key>", self.bindKey)
    def bindKey(self, event):
        key = event.keysym
        if key == "Left" or key == "Right" or key == "Up" or key == "Down":
            if key == "Left":
                self.moveLeft()
            elif key == "Right":
                self.moveRight()
            elif key == "Up":
                self.moveUp()
            elif key == "Down":
                self.moveDown()
            if not self.isFull():
                self.addNewTile() #NOTE: render in addNewTile() instead of here
                self.step += 1
                self.stepLabel["text"] = f"Step: {self.step}"
            if self.isGameOver():
                messagebox.showinfo("Game Over", "Game Over")
    def isGameOver(self):
        if self.isFull() and self.checkHorizontalGameOver() and self.checkVerticalGameOver():
            return True
        return False
    def isFull(self):
        return np.count_nonzero(self.state) == 16
    def checkHorizontalGameOver(self):
        for row in range(4):
            for col in range(3):
                if self.state[row][col] == self.state[row][col+1] and self.state[row][col] != 0:
                    return False
        return True
    def checkVerticalGameOver(self):
        for col in range(4):
            for row in range(3):
                if self.state[row][col] == self.state[row+1][col] and self.state[row][col] != 0:
                    return False
        return True
    def initializeComponents(self):
        #game frame
        self.gameFrame = tk.Frame(self.root, width=500, height=500, background="lavender")
        self.gameFrame.place(x=350, y=120)
        self.gameFrame.grid_propagate(0)

        #title and step label
        self.title = tk.Label(self.root, text="8-puzzle", font=("Arial", 30, "bold"))
        self.title.place(x=560, y=20)
        self.stepLabel = tk.Label(self.root, text=f"Step: 0", font=("Arial", 20))
        self.stepLabel.place(x=350, y=75)
        self.timeLabel = tk.Label(self.root, text=f"Time: {0:.3f}s", font=("Arial", 20))
        self.timeLabel.place(x=680, y=75) #for benchmark

        #button frame
        self.btnFrame = tk.Frame(self.root, width=200, height=500, background="cyan")
        self.btnFrame.place(x=100, y=120)
        self.btnFrame.pack_propagate(0) # don't shrink
        BUTTON_WIDTH = 10
        PADDING = 15
        btnReset = tk.Button(self.btnFrame, text="Reset", font=("Arial", 20), 
                        width=BUTTON_WIDTH, command=lambda: self.initializeTiles(self.state))
        btnReset.pack(pady=PADDING)
        cbAlgo = ttk.Combobox(self.btnFrame, values=["BFS", "DFS", "IDS", "UCS"], font=("Arial", 20), 
                              width=BUTTON_WIDTH, state="readonly")
        # stop control with up and down arrow keys
        cbAlgo.bind("<<ComboboxSelected>>", lambda event: self.root.focus_set())
        cbAlgo.current(0)
        cbAlgo.pack(pady=PADDING)
        btnSolve = tk.Button(self.btnFrame, text="Solve", font=("Arial", 20), 
                     width=BUTTON_WIDTH, command=lambda: self.solve(cbAlgo.get()))
        btnSolve.pack(pady=PADDING)
    def solve(self, algo):
        if algo == "BFS":
            self.solveBFS()
        elif algo == "DFS":
            self.solveDFS()
        elif algo == "IDS":
            self.solveIDS()
        elif algo == "UCS":
            self.solveUCS()
    
    def renderState(self, state):
        # clear the frame
        for widget in self.gameFrame.winfo_children():
            widget.destroy()
        for row in range(4):
            for col in range(4):
                if state[row][col] != 0:
                    Tile(self.gameFrame, state[row][col], row, col)
    def addNewTile(self):
        row = np.random.randint(0, 4)
        col = np.random.randint(0, 4)
        while self.state[row][col] != 0:
            row = np.random.randint(0, 4)
            col = np.random.randint(0, 4)
        self.state[row][col] = 2
        self.renderState(self.state)
    def compressBoard(self): #compress all tiles to the left
        new_state = np.zeros((4, 4), dtype=np.int32)
        for row in range(4):
            pos = 0
            for col in range(4):
                if self.state[row][col] != 0:
                    new_state[row][pos] = self.state[row][col]
                    pos += 1
        self.state = new_state
    def mergeBoard(self): #merge tiles after compressing
        for row in range(4):
            for col in range(3):
                if self.state[row][col] == self.state[row][col+1] and self.state[row][col] != 0:
                    self.state[row][col] *= 2
                    self.state[row][col+1] = 0
    def reverseBoard(self): #reverse the board for moving right
        new_state = np.zeros((4, 4), dtype=np.int32)
        for row in range(4):
            for col in range(4):
                new_state[row][col] = self.state[row][3-col]
        self.state = new_state
    def transposeBoard(self): #transpose the board for moving up, down
        self.state = self.state.T
    def moveLeft(self):
        self.compressBoard()
        self.mergeBoard()
        self.compressBoard()
    def moveRight(self):
        self.reverseBoard()
        self.moveLeft()
        self.reverseBoard()
    def moveUp(self):
        self.transposeBoard()
        self.moveLeft()
        self.transposeBoard()
    def moveDown(self):
        self.transposeBoard()
        self.moveRight()
        self.transposeBoard()
if __name__ == '__main__':
    root = tk.Tk()
    gameplay = Gameplay(root)
    root.mainloop()