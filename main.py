#2048 Game with AI
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
from collections import deque
from PIL import Image, ImageTk
import time
from tile import Tile
from board import Board
class Gameplay:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.title("2048")

        self.initializeComponents()
        self.board = Board()
        self.renderState(self.board.state)
        self.root.bind("<Key>", self.bindKey)
    def bindKey(self, event):
        key = event.keysym
        validKeys = ["Left", "Right", "Up", "Down", "a", "d", "w", "s"]
        if key in validKeys:
            if key == "Left" or key == "a":
                self.board.moveLeft()
            elif key == "Right" or key == "d":
                self.board.moveRight()
            elif key == "Up" or key == "w":
                self.board.moveUp()
            elif key == "Down" or key == "s":
                self.board.moveDown()
            if not self.board.isFull():
                self.board.addNewTile()
                self.renderState(self.board.state)
                
            if self.board.isGameOver():
                messagebox.showinfo("Game Over", "Game Over")
    def initializeComponents(self):
        #game frame
        self.gameFrame = tk.Frame(self.root, width=500, height=500, background="lavender")
        self.gameFrame.place(x=350, y=120)
        self.gameFrame.grid_propagate(0)

        #title and step label
        self.title = tk.Label(self.root, text="2048", font=("Arial", 30, "bold"))
        self.title.place(x=560, y=20)
        self.stepLabel = tk.Label(self.root, text=f"Step: 0", font=("Arial", 20))
        self.stepLabel.place(x=350, y=75)
        self.scoreLabel = tk.Label(self.root, text=f"Score: 0", font=("Arial", 20))
        self.scoreLabel.place(x=680, y=75) #for benchmark

        #button frame
        self.btnFrame = tk.Frame(self.root, width=200, height=500, background="cyan")
        self.btnFrame.place(x=100, y=120)
        self.btnFrame.pack_propagate(0) # don't shrink
        BUTTON_WIDTH = 10
        PADDING = 15
        btnRestart = tk.Button(self.btnFrame, text="Restart", font=("Arial", 20), 
                        width=BUTTON_WIDTH, command=lambda: self.restart())
        btnRestart.pack(pady=PADDING)
        cbAlgo = ttk.Combobox(self.btnFrame, values=["BFS", "DFS", "IDS", "UCS"], font=("Arial", 20), 
                              width=BUTTON_WIDTH, state="readonly")
        # stop control with up and down arrow keys
        cbAlgo.bind("<<ComboboxSelected>>", lambda event: self.root.focus_set())
        cbAlgo.current(0)
        cbAlgo.pack(pady=PADDING)
        btnSolve = tk.Button(self.btnFrame, text="Solve", font=("Arial", 20), 
                     width=BUTTON_WIDTH, command=lambda: self.solve(cbAlgo.get()))
        btnSolve.pack(pady=PADDING)
    def restart(self):
        self.board = Board()
        self.renderState(self.board.state)
    def solve(self, algo):
        if algo == "BFS":
            self.solveBFS()
        elif algo == "DFS":
            self.solveDFS()
        elif algo == "IDS":
            self.solveIDS()
        elif algo == "UCS":
            self.solveUCS()
    def solveDFS(self):
        pass
    def renderState(self, state):
        # clear the frame
        for widget in self.gameFrame.winfo_children():
            widget.destroy()
        for row in range(4):
            for col in range(4):
                if state[row][col] != 0:
                    Tile(self.gameFrame, state[row][col], row, col)
        self.stepLabel["text"] = f"Step: {self.board.step}"
        self.scoreLabel["text"] = f"Score: {self.board.score}"
if __name__ == '__main__':
    root = tk.Tk()
    gameplay = Gameplay(root)
    root.mainloop()