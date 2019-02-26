from tkinter import *
from tkinter import ttk

# Round Rectanle for the canvas
def rounded_rect(self, x, y, w, h, c, fill="black", linetags=None, arctags=None):
    self.create_arc(x,   y,   x+2*c,   y+2*c,   start= 90, extent=90, style="arc", outline=fill, tags=arctags)
    self.create_arc(x+w-2*c, y+h-2*c, x+w, y+h, start=270, extent=90, style="arc", outline=fill, tags=arctags)
    self.create_arc(x+w-2*c, y,   x+w, y+2*c,   start=  0, extent=90, style="arc", outline=fill, tags=arctags)
    self.create_arc(x,   y+h-2*c, x+2*c,   y+h, start=180, extent=90, style="arc", outline=fill, tags=arctags)
    self.create_line(x+c, y,   x+w-c, y    , fill=fill, tags=linetags)
    self.create_line(x+c, y+h, x+w-c, y+h  , fill=fill, tags=linetags)
    self.create_line(x,   y+c, x,     y+h-c, fill=fill, tags=linetags)
    self.create_line(x+w, y+c, x+w,   y+h-c, fill=fill, tags=linetags)
Canvas.create_roundsqaure = rounded_rect


# Circle for the canvas
def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = create_circle


# Define Grid layout
def grid(root,row,column):
    "Defines rows and columns if grid method is used"
    if column:
        for y in range(column): Grid.columnconfigure(root, y, weight=1)
    if row:
        for x in range(row): Grid.rowconfigure(root, x, weight=1)