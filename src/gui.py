import os
import sys
import time

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSignal

from environement import Environement


class App(QWidget):
    """
    The App class hold all the logic needed to have a GUI for the simulation
    """

    CELL_WIDTH = 64
    CELL_HEIGHT = 64
    TITLE = "LAWN MOWER"

    start = pyqtSignal()

    def __init__(self, rows, columns, environement, mowers):
        super().__init__()

        self.rows = rows
        self.columns = columns
        self.cells = {}
        self.cell_to_image = {}

        self.environement = environement
        self.mowers = mowers

        self.setup_images()
        self.setup_ui()

    def setup_images(self):
        """
        Fucntion that setup the binding between environment cell calue and image
        """
        src_path = os.path.dirname(os.path.abspath(__file__))
        self.cell_to_image[Environement.GRASS] = os.path.join(
            src_path, 'img', 'grass.jpeg')
        self.cell_to_image[Environement.MOWED_GRASS] = None
        self.cell_to_image[Environement.MOWER_N] = os.path.join(
            src_path, 'img', 'mower_N.png')
        self.cell_to_image[Environement.MOWER_E] = os.path.join(
            src_path, 'img', 'mower_E.png')
        self.cell_to_image[Environement.MOWER_S] = os.path.join(
            src_path, 'img', 'mower_S.png')
        self.cell_to_image[Environement.MOWER_W] = os.path.join(
            src_path, 'img', 'mower_W.png')

    def setup_ui(self):
        """
        Setup all the widget we need
        """
        self.setWindowTitle(self.TITLE)
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        buttons = QHBoxLayout()

        for column in range(self.columns):
            for row in range(self.rows):
                # Create widget
                label = QLabel()
                label.setStyleSheet(
                    "QLabel { background-color : rgb(2,179,2); }")
                grid.addWidget(label, row, column)
                self.cells[column, row] = label

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start.emit)
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(QCoreApplication.instance().quit)
        buttons.addWidget(start_btn)
        buttons.addWidget(exit_btn)

        layout.addLayout(grid)
        layout.addLayout(buttons)

        self.setLayout(layout)

        self.redraw()
        self.show()

    def create_pixmap(self, cell_type):
        """
        Create a QPixmap from a cell type
        @param cell_type: Environement.MOWER_[N|E|S|W] | Environement.GRASS | Environement.MOWED_GRASS
        @return: QPixMap. Scaled at right CELL_WIDTH and CELL_HEIGHT or None
        """
        file_path = self.cell_to_image[cell_type]
        if file_path:
            pixmap = QPixmap(file_path)
            return pixmap.scaled(self.CELL_WIDTH, self.CELL_HEIGHT)
        return None

    def update_cell(self, x, y, pixmap):
        """
        Update cell image using a QPixmap widget
        @param x: Integer - X coordinate
        @param y: Integer - Y coordinate
        @param pixmap: QPixmap the image we want to put in the cell

        """
        label = self.cells[x, y]
        label.clear()
        if pixmap:
            label.setPixmap(pixmap)

    def redraw(self):
        """
        Redraw all images on grid
        @param env: Environement
        """
        for x in range(self.columns):
            for y in range(self.rows):
                x1, y1 = self.environement.transpose_coordinates(x, y)
                cell = self.environement.get_cell(x1, y1)
                pixmap = self.create_pixmap(cell)
                self.update_cell(x, y, pixmap)
