import logging
import sys

from mower import Mower
from parser import Parser
from environement import Environement

DEFAULT_INPUT_FILE_PATH = "input.txt"


class Simulation:

    def __init__(self, input_file, logs=False, gui=False):

        self.logs = logs
        self.gui = gui

        self.parser = Parser(input_file)

        self.environement = None
        self.mowers = []

        self._set_up()

    def _set_up(self):

        self.parser.parse()
        width, height = self.parser.grid_size
        print(width, height)
        self.environement = Environement(width, height)

        # Creating mowers
        for mower_dict in self.parser.mowers:
            new_mower = Mower(**mower_dict, environment=self.environement)
            self.mowers.append(new_mower)

    def run(self):
        for m in self.mowers:
            m.process()
            print(m.current_position, m.current_orientation)


if __name__ == '__main__':

    # Configure logger
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    simulation = Simulation(DEFAULT_INPUT_FILE_PATH)
    simulation.run()
