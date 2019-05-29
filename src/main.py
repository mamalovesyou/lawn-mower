import logging
import time
import sys

from gui import App
from mower import Mower
from parser import Parser
from threading import Thread
from environement import Environement

from PyQt5.QtWidgets import QApplication

DEFAULT_INPUT_FILE_PATH = "input.txt"


class Simulation:

    def __init__(self, input_file, logs=False, gui=False):

        self.logs = logs
        self.gui = False

        self.parser = Parser(input_file)

        self.environement = None
        self.mowers = []

        self._setup()

    def _setup(self):

        self.parser.parse()
        self.width, self.height = self.parser.grid_size
        self.environement = Environement(self.width, self.height)

        # Creating mowers
        for mower_dict in self.parser.mowers:
            new_mower = Mower(
                **mower_dict, environment=self.environement, logs=self.logs)
            self.mowers.append(new_mower)

    def setup_gui(self):
        self.gui = App(self.width, self.height, self.environement, self.mowers)
        self.gui.started.connect(self.setup_thread)
        return gui

    def setup_thread(self):
        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        for m in self.mowers:
            for p, o in m:
                if self.gui:
                    time.sleep(0.2)
                    self.gui.redraw()
            print(p, o)


if __name__ == '__main__':

    logs = False
    gui = False

    # CLI
    for index, arg in enumerate(sys.argv):
        if arg in ['--logs', '-l']:
            logs = True
            # Configure logger
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        if arg in ['--gui']:
            gui = True

    simulation = Simulation(DEFAULT_INPUT_FILE_PATH, logs=logs)

    if gui:
        app = QApplication(sys.argv)
        widget = simulation.setup_gui()
        sys.exit(app.exec_())

    else:
        simulation.run()
