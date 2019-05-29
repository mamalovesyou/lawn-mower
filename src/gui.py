import os
import sys
import time

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap

from environement import Environement


class App(QWidget):

    CELL_WIDTH = 64
    CELL_HEIGHT = 64
    TITLE = "LAWN MOWER"

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
        self.cell_to_image[Environement.MOWED_GRASS] = os.path.join(
            src_path, 'img', 'mowed_grass.jpg')
        self.cell_to_image[Environement.MOWER_N] = os.path.join(
            src_path, 'img', 'mower_N.png')
        self.cell_to_image[Environement.MOWER_E] = os.path.join(
            src_path, 'img', 'mower_E.png')
        self.cell_to_image[Environement.MOWER_S] = os.path.join(
            src_path, 'img', 'mower_S.png')
        self.cell_to_image[Environement.MOWER_W] = os.path.join(
            src_path, 'img', 'mower_W.png')

    def setup_ui(self):
        self.setWindowTitle(self.TITLE)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        for column in range(self.columns):
            for row in range(self.rows):
                # Create widget
                label = QLabel()
                pixmap = self.create_pixmap(Environement.GRASS)
                label.setPixmap(pixmap)
                self.layout.addWidget(label, row, column)
                self.cells[row, column] = label

        self.show()

    def create_pixmap(self, cell_type):
        """
        Create a QPixmap from a cell type
        @param cell_type: Environement.MOWER_[N|E|S|W] | Environement.GRASS | Environement.MOWED_GRASS
        @return: QPixMap. Scaled at right CELL_WIDTH and CELL_HEIGHT
        """
        file_path = self.cell_to_image[cell_type]
        pixmap = QPixmap(file_path)
        return pixmap.scaled(self.CELL_WIDTH, self.CELL_HEIGHT)

    def update_cell(self, x, y, pixmap):
        """
        Update cell image using a QPixmap widget
        """
        label = self.cells[x, y]
        label.clear()
        label.setPixmap(pixmap)

    def redraw(self):
        """
        Redraw all images on grid
        @param env: Environement
        """
        for x in range(self.rows):
            for y in range(self.columns):
                cell = self.environement.get_cell(x, y)
                pixmap = self.create_pixmap(cell)
                self.update_cell(x, y, pixmap)

    def start(self):
        for m in self.mowers:
            for p, o in m:
                time.sleep(1)
                self.redraw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App(6, 6, [])
    sys.exit(app.exec_())
