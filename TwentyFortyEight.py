"""
Clone of 2048 game.
"""

from random import randint
import poc_2048_gui        

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = [0] * len(line)
    merged = [False] * len(line)    
    for count in range(len(line)):
        result[count] = 0
        merged[count] = False       
        for line_count in range(len(line)):
            if line[line_count] != 0:
                for result_count in range(len(line)):
                    if (result[result_count] == 0):
                        result[result_count] = line[line_count]
                        break        
        for result_count2 in range(len(line) - 1):
            if result[result_count2] == result[result_count2 + 1] and merged[result_count2] == False:
                result[result_count2] *= 2
                merged[result_count2] = True                
                for result_count3 in range(result_count2 + 1, len(line) - 1):
                    result[result_count3] = result[result_count3 + 1]
                result[len(line) - 1] = 0
        return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._board = [0][0]
        self.reset() 
        self._initial_indices = {
                                 UP: [(0, col) for col in range(self._grid_width)],
                                 DOWN: [(self._grid_height - 1, col) for col in range(self._grid_width)],
                                 LEFT: [(row, 0) for row in range(self._grid_height)],
                                 RIGHT: [(row, self._grid_width - 1) for row in range(self._grid_height)]
                                 }
        
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self._board = [[0 for dummy_width in xrange(self._grid_width)] for dummy_height in xrange(self._grid_height)]
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
    
    def _can_move(self):
        """
        Determines whether the player can move
        Returns a boolean
        """
        is_full = True
        top_bottom = False
        left_right = False
        for row in range(len(self._board) - 1):
            for col in range(len(self._board[0]) - 1):
                if self._board[row][col] == self._board[row][col + 1] or self._board[row + 1][col] == self._board[row + 1][col + 1]:
                    left_right = True
                if self._board[row][col] == self._board[row + 1][col] or self._board[row][col + 1] == self._board[row + 1][col + 1]:
                    top_bottom = True
        
        for row in range(len(self._board)):
            for col in range(len(self._board[0])):
                if self._board[row][col] == 0:
                    is_full = False
                    
        if is_full == True and top_bottom == False and left_right == False:
            return False
        else:
            return True
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        for dummy_row in range(self._grid_height):
            for dummy_col in range(self._grid_width):
                if self._board[dummy_row][dummy_col] == 2048:
                    print "Congratulations! You win!"

        has_changed = False
        
        for tile in self._initial_indices[direction]:
            temp_list = []
            dummy_list = []
            row = tile[0]
            col = tile[1]
            
            while (0 <= row and row < self._grid_height) and (0 <= col and col < self._grid_width):
                temp_list.append(self._board[row][col])
                dummy_list.append((row, col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
                
            temp_list = merge(temp_list)
            for index in range(len(dummy_list)):
                if self._board[dummy_list[index][0]][dummy_list[index][1]] != temp_list[index]:
                    has_changed = True
                self.set_tile(dummy_list[index][0], dummy_list[index][1], temp_list[index])

        if has_changed == True:
            self.new_tile()
            
        if self._can_move() == False:
            print "Board is full with no legal moves. GAME OVER"
                    
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        random_row = randint(0, self._grid_height - 1)
        random_col = randint(0, self._grid_width - 1)
        while self._board[random_row][random_col] != 0:
            random_row = randint(0, self._grid_height - 1)
            random_col = randint(0, self._grid_width - 1)
            
        chance = randint(1, 10)
        if chance == 1:
            self.set_tile(random_row, random_col, 4)
        else:
            self.set_tile(random_row, random_col, 2)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self._board[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

