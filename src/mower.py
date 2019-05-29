import logging
import operator

from collections import deque


class Mower:
    """
    Mower class
    """

    ORIENTATIONS = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    INSTRUCTIONS = {'L': -1, 'R': +1, 'F': 0}

    def __init__(self, id, position, orientation, instructions, environment, logs):

        # Create logger
        self.id = id
        self.name = "Mower-{}".format(self.id)

        self.logs = logs
        if self.logs:
            self.logger = logging.getLogger(self.name)

        self._available_orientations = list(self.ORIENTATIONS.keys())

        self.current_position = position
        self.current_orientation = orientation
        self.instructions = instructions
        self.current_instruction_index = 0

        self.environement = environment

    def __iter__(self):
        """
        Implement mower's logic as an iterator.
        """
        while self.current_instruction_index < len(self.instructions):
            instruction = self.instructions[self.current_instruction_index]
            if self.logs:
                self.logger.info(
                    "Preparing processing intructions: %s", instruction)
            self._process_instruction(instruction)
            self.current_instruction_index += 1
            yield self.current_position, self.current_orientation

    def _process_instruction(self, instruction):
        """
        Process instruction
        """
        if instruction not in self.INSTRUCTIONS.keys():
            if self.logs:
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

        if self.logs:
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
            if self.logs:
                self.logger.info("Performing F (Forward) instruction. From: (%s, %s) -> To: (%s, %s)",
                                 self.current_position, self.current_orientation,
                                 new_position, self.current_orientation)
            self.current_position = new_position

            # Update environement
            self.environement.update_cell(
                *new_position, self.current_orientation)
        else:
            if self.logs:
                self.logger.info(
                    "Skipping F instruction. %s is out of field.", new_position)
