#!/usr/bin/python3

import tkinter
import random


class App(tkinter.Tk):

    COLORS = {
        'MOWED_GRASS': '#7CFC00',
        'GRASS': '#006400'
    }

    def __init__(self, rows, columns, mowers, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.rows = rows
        self.columns = columns

        self.cellwidth = 64
        self.cellheight = 64

        window_width = (self.columns + 1) * self.cellwidth
        window_height = (self.rows + 1) * self.cellheight

        self.canvas = tkinter.Canvas(
            self, width=window_width, height=window_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        self.cells = {}
        self.mowers = {}

        for column in range(self.columns + 1):
            for row in range(self.rows + 1):
                x1, y1 = self.scale_coordinates(column, row)
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.cells[row, column] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.COLORS['GRASS'], tags="grass")

        for m in mowers:
            x, y = m.current_position
            print(x, y)
            new_x, new_y = self.transpose_coordinates(x, y)
            print(new_x, new_y)
            self._create_mower(m.id, new_x, new_y)

    def update_mower(self, mower):
        """
        Update mower position on the grid
        """

        mower_id = mower.id
        x, y = mower.current_position
        row, column = self.transpose_coordinates(x, y)

        current_pos = self.mowers[mower_id]['coords']
        mowed_grass_id = self.cells[current_pos[0], current_pos[1]]
        self.canvas.itemconfig(mowed_grass_id, tags='mowed_grass')

        # mower_cell_id = self.cells[row, column]
        # self.canvas.itemconfig(mower_cell_id, tags='mowed_grass')

        x1, y1 = self.scale_coordinates(row, column)
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight

        self.canvas.coords(self.mowers[mower_id]
                           ['canvas'], x1+2, y1+2, x2-2, y2-2)

        self.redraw()

    def _create_mower(self, mower_id, x, y):
        x1, y1 = self.scale_coordinates(x, y)
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight
        self.mowers[mower_id] = {}
        self.mowers[mower_id]['canvas'] = self.canvas.create_oval(
            x1+2, y1+2, x2-2, y2-2, fill="black", tags="mower")
        self.mowers[mower_id]['coords'] = (x, y)

    def scale_coordinates(self, x, y):
        """
        This function scale coordinates for the canvas
        @param x: It will become x * cellWidth
        @param y: It will become y * cellWidth 
        @return: Tuple of integer
        """
        return x * self.cellwidth, y * self.cellheight

    def transpose_coordinates(self, x, y):
        """
        This function trnaspose coordiantes from top left origin
        to a bottom left origin
        @param x: No change needed
        @param y: It will be transposed as windowHeight - y 
        @return: Tuple of integer 
        """
        return x, self.rows - y

    def redraw(self):
        self.canvas.itemconfig("grass", fill=self.COLORS['GRASS'])
        self.canvas.itemconfig("mowed_grass", fill=self.COLORS['MOWED_GRASS'])
        self.canvas.itemconfig("mower", fill='black')


if __name__ == "__main__":
    app = App()
    app.mainloop()
