import logging
import sys

from gui import App
from mower import Mower
from parser import Parser
from environement import Environement

from PyQt5.QtWidgets import QApplication

DEFAULT_INPUT_FILE_PATH = "input.txt"


class Simulation:

    def __init__(self, input_file, logs=False, gui=False):

        self.logs = logs
        self.gui = gui

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

    def run(self):

        if self.gui:
            app = QApplication(sys.argv)
            ex = App(self.width, self.height, self.environement, self.mowers)
            ex.start()
            sys.exit(app.exec_())

        else:
            for m in self.mowers:
                for p, o in m:
                    pass
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

    simulation = Simulation(DEFAULT_INPUT_FILE_PATH, logs=logs, gui=gui)
    simulation.run()
