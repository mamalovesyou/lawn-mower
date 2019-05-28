import logging
import operator
from collections import deque

class Mower:
    """
    Mower class
    """
     
    ORIENTATIONS = {'N': (0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}
    INSTRUCTIONS = {'L': -1, 'R': +1, 'F':0}

    def __init__(self, identifier, init_position, init_orientation, instructions):

        # Create logger
        self.id = identifier
        self.name = "Mower-{}".format(identifier)
        self.logger = logging.getLogger(self.name)

        self._available_orientations = list(self.ORIENTATIONS.keys())

        self.initial_position = init_position
        self.initial_orientation = init_orientation
        self.current_position = init_position
        self.current_orientation = init_orientation
        self.instructions = instructions

    def process(self):
        """
        Implement the logic for the next instruction
        """
        # Dequeue list of instructions
        self.logger.info("Preparing processing intructions")
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

        self.logger.error("Performing %s instruction. From: (%s, %s) -> To: (%s, %s)", 
                            instruction, self.current_position, self.current_orientation, 
                            self.current_position, new_orientation)

        self.current_orientation = self._available_orientations[index]
    
    def _process_instruction_forward(self):
        """
        Process forward instructions
        """
        coords_increment = self.ORIENTATIONS[self.current_orientation]
        new_position = tuple(map(operator.add, self.current_position,coords_increment))
        self.current_position = new_position
        self.logger.error("Performing F (Forward) instruction. From: (%s, %s) -> To: (%s, %s)", 
                            self.current_position, self.current_orientation, 
                            new_position, self.current_orientation)
        self.current_position = new_position
        
        


        
        

