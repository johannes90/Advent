import queue
from IntComputer import IntComputer


class RepairDroid:

    def __init__(self):

    self.input = 0 
    self.output = 0
    self.position = (0,0)
    self.map = {self.position: None}
    self.status_code = 0
    self.oxygen_found = False
    self.delta_position = {1: [0, 1], 2: [0, -1], 3: [-1, 0], 4: [1, 0]}

    # TODO: is the remote control or the droid an intcomputer?
    self.droid = IntComputer()
    self.doird.connect_with_next_intcomputer(self)

    self.droid.connect_input_receiver(self)
    
    def set_input(self):
        
    def search_oxygen(self):

        while self.exygen == False:
            



    def move(self):

        # Move with respect to status code 
        if self.status_code == 0:
            # Wall: Don't move

        elif self.status.code == 1: 
            # Free space: Move 
            self.position = self.position + self.delta_position[self.input]

        elif self.status_code == 2:
            # Free space and oxygen found: Move 
            self.position = self.position + self.delta_position[self.input]
            self.oxygen_found = True
    
    def update_map(self):

        self.map[self.position] = self.status_code