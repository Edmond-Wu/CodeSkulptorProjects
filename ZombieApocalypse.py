"""
Zombie Apocalypse Simulator mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(poc_grid.Grid.get_grid_height(self), poc_grid.Grid.get_grid_width(self))
        distance_field = [[poc_grid.Grid.get_grid_height(self) * poc_grid.Grid.get_grid_width(self) for dummy_col in range(poc_grid.Grid.get_grid_width(self))]
                       for dummy_row in range(poc_grid.Grid.get_grid_height(self))]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        else:
            for human in self._human_list:
                boundary.enqueue(human)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        while boundary:
            current_cell = boundary.dequeue()
            distance = distance_field[current_cell[0]][current_cell[1]] + 1
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    if self.is_empty(neighbor[0], neighbor[1]):
                        distance_field[neighbor[0]][neighbor[1]] = distance
                        boundary.enqueue(neighbor)
                        
        return distance_field
  
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        temp_human_list = []
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            max_distance = 0
            temp_neighbors = []
            temp_neighbors.append(human)
            for neighbor in neighbors:
                distance = zombie_distance[neighbor[0]][neighbor[1]]
                self_dist = zombie_distance[human[0]][human[1]]
                if distance > max_distance and distance > self_dist and self.is_empty(neighbor[0], neighbor[1]):
                    max_distance = distance
                    temp_neighbors = []
                if zombie_distance[neighbor[0]][neighbor[1]] == max_distance and self.is_empty(neighbor[0], neighbor[1]):
                    temp_neighbors.append(neighbor)
            choice = random.choice(temp_neighbors)
            temp_human_list.append(choice)
        self._human_list = temp_human_list
            
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp_zombie_list = []
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            min_distance = self.get_grid_width() * self.get_grid_height()
            temp_neighbors = []
            temp_neighbors.append(zombie)
            for neighbor in neighbors:
                distance = human_distance[neighbor[0]][neighbor[1]]
                self_dist = human_distance[zombie[0]][zombie[1]]
                if distance < min_distance and distance < self_dist and self.is_empty(neighbor[0], neighbor[1]):
                    min_distance = distance
                    temp_neighbors = []
                if human_distance[neighbor[0]][neighbor[1]] == min_distance and self.is_empty(neighbor[0], neighbor[1]):
                    temp_neighbors.append(neighbor)
            choice = random.choice(temp_neighbors)
            temp_zombie_list.append(choice)
        self._zombie_list = temp_zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))

