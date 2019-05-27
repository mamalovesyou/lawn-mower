import logging
import sys

from mower import Mower
from gui import App


class InputParser:

    DEFAULT_INPUT_FILE_PATH = "input.txt"

    def __init__(self, input_file=None):
        if input_file:
            self._input_file = input_file
        else:
            self._input_file = self.DEFAULT_INPUT_FILE_PATH

        self.grid_size = (None, None)
        self.mowers = []

    def parse(self):
        with open(self._input_file, 'r') as fp:
            # First line is always grid size
            line = fp.readline()
            self.grid_size = self.get_grid_size(line)

            # Load mowers infos (every 2 lines this is a new mower)
            mowers = fp.readlines()
            for i in range(0, len(mowers), 2):
                print(mowers[i], mowers[i+1])
                initial_position = mowers[i].rstrip()
                coords, orientation = self.get_mower_position(initial_position)
                new_mower = Mower(i, coords, orientation, mowers[i+1].rstrip())
                self.mowers.append(new_mower)

    def get_grid_size(self, size_str):
        """
        Return the size of a grid as a tuple of integer. (height, width)
        @param size_str: Size of the grid as string. (ex: '5 5')
        @return: Tuple of integer (height, width) or None if parsing error
        """
        dimensions = size_str.split(' ')

        # Parsing error
        if len(dimensions) != 2:
            return (None, None)

        return tuple(map(int, dimensions))

    def get_mower_position(self, position_str):

        # Split string using space char
        position = position_str.split(' ')

        # Parsing error
        if len(position) != 3:
            return None, None

        # Mower's coords are 2 first elements in the list
        coords = tuple(map(int, position[:2]))

        # Orientation is always last in the list
        orientation = position[-1]
        return coords, orientation


if __name__ == '__main__':

    # Configure logger
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    input_parser = InputParser()
    input_parser.parse()
    size = input_parser.grid_size
    mowers = input_parser.mowers

    # Configure GUI
    # app = App(size[0], size[1], mowers)

    for m in mowers:
        m.process()
        # app.after(3000, lambda: app.update_mower(m))

    # app.mainloop()
