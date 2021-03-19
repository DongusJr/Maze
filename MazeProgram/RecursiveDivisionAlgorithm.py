from Maze import Maze
import random
# random.seed(2)

EMPTY, DOWN, RIGHT, FULL = 0, 1, 2, 3
HORIZONTAL = 1
VERTICAL = 2

class RecursiveDivisionAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width, True)
        self.c_x, self.c_y = -1, -1
        for i in range(self.height):
            self.grid[i][-1] |= 2
        for i in range(self.width):
            self.grid[-1][i] |= 1
    
    def choose_orientation(self, height, width):
        if width < height:
            return HORIZONTAL
        elif height < width:
            return VERTICAL
        else:
            return HORIZONTAL if random.randint(0,1) == 0 else VERTICAL

    def fill_maze(self):
        self.display_maze()
        self.divide(0,0, self.height, self.width,self.choose_orientation(self.height, self.width))
        

    def divide(self, x, y, height, width, orientation):
        if width < 2 or height < 2:
            return None

        go_horizontal = orientation == HORIZONTAL
        wx = x + (0 if go_horizontal else random.randint(0, width - 2))
        wy = y + (random.randint(0, height - 2) if go_horizontal else 0)

        px = wx + (random.randint(0, width - 2) if go_horizontal else 0)
        py = wy + (0 if go_horizontal else random.randint(0, height - 2))

        dx = 1 if go_horizontal else 0
        dy = 0 if go_horizontal else 1

        length = width if go_horizontal else height

        direction = DOWN if go_horizontal else RIGHT
        
        for i in range(length):
            self.add_direction_to_grid(wy, wx, direction)
            wx += dx
            wy += dy

        self.display_maze()
        self.grid[py][px] = self.grid[py][px] ^ direction
        self.display_maze()

        nx, ny = x, y
        w, h = [width, wy - y + 1] if go_horizontal else [wx - x + 1, height]
        self.divide(nx, ny, h, w, self.choose_orientation(h, w))

        nx, ny = [x, wy + 1] if go_horizontal else [wx + 1, y]
        w, h = [width, y + height - wy - 1] if go_horizontal else [x + width - wx - 1, height]
        self.divide(nx, ny, h, w, self.choose_orientation(h, w))

if __name__ == "__main__":
    maze = RecursiveDivisionAlgorithm(25,25)
    maze.fill_maze()
