from Maze import Maze
import random
from randomdict import RandomDict
# random.seed(2)

N, S, W, E = 1, 2, 4, 8
IN = 16

class WilsonsAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)
        self.available_cells = self._make_available_cells()
        self.path_grid = [[True]*width for _ in range(height)]

    def _make_available_cells(self):
        avail_cells = RandomDict()
        k = 0
        for y in range(self.height):
            for x in range(self.width):
                avail_cells[k] = (y,x)
                k += 1
        return avail_cells
    
    def fill_maze(self):
        y, x = self.available_cells.random_value()
        del self.available_cells[y*self.width + x]
        self.add_direction_to_grid(y, x, IN)
        self.mark_grid(y, x, False)

        remaining = self.width * self.height - 1

        while remaining > 0:
            for x, y, direction in self.walk():
                self.set_x_and_y(y,x)
                nx, ny = (x + self.move_x[direction]), (y + self.move_y[direction])
                self.add_direction_to_grid(y, x, direction)
                self.add_direction_to_grid(ny, nx, self.opposite[direction])
                self.mark_grid(y, x, False)
                self.display_maze()
                remaining -= 1
        self.c_x, self.c_y = -1, -1
        self.foreground_grid = [[False]*self.width for i in range(self.height)]
        self.display_maze()

    def walk(self):
        self.c_y, self.c_x = self.available_cells.random_value()
        visits = {(self.c_x, self.c_y) : 0}
        self.foreground_grid = [[False]*self.width for i in range(self.height)]
        start_x, start_y = self.c_x, self.c_y
        walking = True
        directions = [N, S, W, E]
        while walking:
            walking = False
            random.shuffle(directions)
            for direction in directions:
                nx, ny = (self.c_x + self.move_x[direction]), (self.c_y + self.move_y[direction])
                if self.is_in_grid(ny, nx):
                    visits[(self.c_x, self.c_y)] = direction
                    self.foreground_grid[self.c_y][self.c_x] = True
                    self.display_maze()
                    if self.get_cell(ny, nx) != 0:
                        break
                    else:
                        self.c_x, self.c_y = nx, ny
                        walking = True
                        break
        
        path = []
        x, y = start_x, start_y
        while True:
            try:
                direction = visits[(x,y)]
            except:
                break
            del self.available_cells[y*self.width + x]
            path.append((x, y, direction))
            x,y = (x + self.move_x[direction]), (y + self.move_y[direction])
        return path

if __name__ == "__main__":
    maze = WilsonsAlgorithm(25, 25)
    maze.fill_maze()