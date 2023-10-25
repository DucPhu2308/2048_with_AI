import numpy as np
class Board:
    def __init__(self):
        self.state = np.zeros((4, 4), dtype=np.int32)
        self.step = 0
        self.score = 0
        self.addNewTile()
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
    def addNewTile(self):
        row = np.random.randint(0, 4)
        col = np.random.randint(0, 4)
        while self.state[row][col] != 0:
            row = np.random.randint(0, 4)
            col = np.random.randint(0, 4)
        self.state[row][col] = 2
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
                    #update score
                    self.score += self.state[row][col]
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
        self.step += 1
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