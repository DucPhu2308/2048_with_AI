import tkinter as tk
colors = {
    2: "white",
    4: "light yellow",
    8: "yellow",
    16: "orange",
    32: "dark orange",
    64: "pink",
    128: "light green",
    256: "green",
    512: "light blue",
    1024: "blue",
    2048: "purple"
}
class Tile:
    def __init__(self, gameFrame, value, row, col):
        self.value = value
        self.gameFrame = gameFrame

        PADDING = 2
        self.gameFrame.update_idletasks()
        frameWidth = self.gameFrame.winfo_width()
        frameHeight = self.gameFrame.winfo_height()
        lableWidth = frameWidth // 4 - PADDING*3
        lableHeight = frameHeight // 4 - PADDING*3
        x = col*(lableWidth + PADDING*3) + PADDING
        y = row*(lableHeight + PADDING*3) + PADDING
                              
        blankImg = tk.PhotoImage()
        self.label = tk.Label(self.gameFrame, text=str(self.value), font=("Arial", 45),
                                 width=lableWidth, height=lableHeight, image=blankImg, compound="c",
                                 border=1, borderwidth=1, relief="solid",
                                 background=colors[self.value], foreground="black")
        # self.label.grid(row=2, column=2, padx=PADDING, pady=PADDING)
        self.label.place(x=x, y=y)
