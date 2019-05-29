
class Parser:
    """
    This class provide a set of methods to extract infos from an input file
    such as:
        - Grid size (width, height)
        - Numbers of mower
        - Mower's initial position 
        - Mower's initial orientation
        - Mower's instructions
    """

    def __init__(self, input_file=None):
        """
        Consutructor method that initialized parser
        """
        self._input_file = input_file
        self.grid_size = (None, None)  # (width, height)
        self.mowers = []

    def parse(self):
        """
        Parse informations from input_file and will extract:
            - Grid size
            - Mower's informations
        It will create a list of mowers
        """

        with open(self._input_file, 'r') as fp:
            # First line is always grid size
            line = fp.readline()
            self.grid_size = self._extract_grid_size(line)

            # Load mowers infos (every 2 lines this is a new mower)
            mowers = fp.readlines()
            for i in range(0, len(mowers), 2):

                initial_position = mowers[i]  # Position line
                instructions = mowers[i+1]  # Instruction line

                # Extract initital_position and orientation
                coords, orientation = self._extract_mower_position(
                    initial_position)
                new_mower = {'id': i, 'position': coords, 'orientation': orientation,
                             'instructions': instructions}
                self.mowers.append(new_mower)

    def _extract_grid_size(self, size_str):
        """
        Return the size of a grid as a tuple of integer. (height, width)
        @param size_str: Size of the grid as string. (ex: '5 5')
        @return: Tuple of integer (height, width) or None if parsing error
        """
        dimensions = size_str.rstrip().split(' ')

        # Parsing error
        if len(dimensions) != 2:
            return (None, None)

        # We need to add 1 because the size is not provided
        # What is provided is (maxX, maxY) and origin is (0, 0)
        result = [int(i) + 1 for i in dimensions]
        return tuple(result)

    def _extract_mower_position(self, position_str):
        """
        This function extract a mower position and orientation
        @param position_str: Format of this string should be 'x y N' 
                             where N is cardinal orientation

        @return: Tuple like (x, y), orientation or (None, None), None if parsing error
        """

        # Split string using space char
        position = position_str.rstrip().split(' ')

        # Parsing error
        if len(position) != 3:
            return (None, None), None

        # Mower's coords are 2 first elements in the list
        coords = tuple(map(int, position[:2]))

        # Orientation is always last in the list
        orientation = position[-1]

        return coords, orientation
