import logging
import time
import sys

from gui import App
from mower import Mower
from parser import Parser
from threading import Thread
from environment import Environment

from PyQt5.QtWidgets import QApplication

DEFAULT_INPUT_FILE_PATH = "input.txt"


class Simulation:
    """
    Simple class used to organized things better.
    """

    def __init__(self, input_file, logs=False, gui=False):

        self.logs = logs
        self.gui = False

        self.parser = Parser(input_file)

        self.environment = None
        self.mowers = []

        self._setup()

    def _setup(self):
        """
        Parse info and instructions using the Parser.
        Create the environment and the mowers
        """
        self.parser.parse()
        self.width, self.height = self.parser.grid_size
        self.environment = Environment(self.width, self.height)

        # Creating mowers
        for mower_dict in self.parser.mowers:
            new_mower = Mower(
                **mower_dict, environment=self.environment, logs=self.logs)
            self.mowers.append(new_mower)

    def setup_gui(self):
        """
        Create the GUI application and connect its start signal to the thread creation
        @return: QWidget. Widget that hold the field and buttons to play with simulation
        """
        self.gui = App(self.width, self.height, self.environment, self.mowers)
        self.gui.start.connect(self.setup_thread)
        return gui

    def setup_thread(self):
        """
        Create a thread to run the simulation.
        It's needed when GUI is needed.
        """
        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        """
        Run the simulation. It basicaly means to iterate over all mower's instructions
        sequentialy. It print the mower position and its orientation after last 
        instruction. It also update the gui if needed.
        """
        for m in self.mowers:
            for p, o in m:
                if self.gui:
                    time.sleep(0.2)
                    self.gui.redraw()

            # Print output
            print("{} {} {}".format(*p, o))


# Entrypoint
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

    # Create the simulation
    simulation = Simulation(DEFAULT_INPUT_FILE_PATH, logs=logs)

    if gui:
        app = QApplication(sys.argv)
        widget = simulation.setup_gui()
        sys.exit(app.exec_())

    else:
        simulation.run()
