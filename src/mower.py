import logging
import operator

from collections import deque


class Mower:
    """
    Mower class
    """

    ORIENTATIONS = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    INSTRUCTIONS = {'L': -1, 'R': +1, 'F': 0}

    def __init__(self, id, position, orientation, instructions, environment):

        # Create logger
        self.id = id
        self.name = "Mower-{}".format(self.id)

        self.logger = logging.getLogger(self.name)
        # else:
        #    self.logger = None

        self._available_orientations = list(self.ORIENTATIONS.keys())

        self.current_position = position
        self.current_orientation = orientation
        self.instructions = instructions
        self.current_instruction_index = 0

        self.environement = environment

    def process(self):
        """
        Implement the logic for the next instruction
        """
        # Dequeue list of instructions
        self.logger.info(
            "Preparing processing intructions: %s", self.instructions)
        for i in self.instructions:
            self._process_instruction(i)

    def _process_instruction(self, instruction):
        """
        Process instruction
        """
        if instruction not in self.INSTRUCTIONS.keys():
            self.logger.error("Instruction %s unknown", instruction)
            return

        # Case where it's a forward instruction
        if instruction == 'F':
            return self._process_instruction_forward()

        # Process a reorientation of the mower
        index = self._available_orientations.index(self.current_orientation)
        index += self.INSTRUCTIONS[instruction]
        if index < 0:
            index = len(self._available_orientations) - 1
        elif index >= len(self._available_orientations):
            index = 0
        new_orientation = self._available_orientations[index]

        self.logger.info("Performing %s instruction. From: (%s, %s) -> To: (%s, %s)",
                         instruction, self.current_position, self.current_orientation,
                         self.current_position, new_orientation)

        self.current_orientation = self._available_orientations[index]

    def _is_valid_move(self, position_to_move):
        """
        Return true is the position to move is valid, False either
        @param position_to_move: tuple(int, int)
        @return: True or False
        """
        return self.environement.is_in_field(*position_to_move)

    def _process_instruction_forward(self):
        """
        Process forward instructions
        """
        coords_increment = self.ORIENTATIONS[self.current_orientation]
        new_position = tuple(
            map(operator.add, self.current_position, coords_increment))

        if self._is_valid_move(new_position):
            self.current_position = new_position
            self.logger.info("Performing F (Forward) instruction. From: (%s, %s) -> To: (%s, %s)",
                             self.current_position, self.current_orientation,
                             new_position, self.current_orientation)
            self.current_position = new_position
        else:
            self.logger.info(
                "Skipping F instruction. %s is out of field.", new_position)
