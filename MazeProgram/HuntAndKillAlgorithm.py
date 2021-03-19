from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8

class HuntAndKillAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)

    def fill_maze(self):
        empty_rows = 0

        while True:
            self.display_maze()
            self.c_x, self.c_y = self.walk()
            if self.c_x == None:
                self.c_x, self.c_y, empty_rows = self.hunt(empty_rows)
            if self.c_x == None:
                break
        self.display_maze() 

    def walk(self):
        directions = [N, S, W, E]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = (self.c_x + self.move_x[direction]), (self.c_y + self.move_y[direction])
            if self.is_in_grid(ny, nx) and not self.grid_is_marked(ny, nx):
                self.add_direction_to_grid(self.c_y, self.c_x, direction)
                self.add_direction_to_grid(ny, nx, self.opposite[direction])
                return (nx, ny)

        return (None, None)

    def hunt(self, empty_rows):
        for y in range(empty_rows, self.height):
            full_cells = 0
            self.mark_a_line(y, True)
            self.display_maze()
            for x in range(self.width):
                neighbours = []
                cell = self.get_cell(y, x)
                if cell != 0:
                    full_cells += 1
                    continue
                else:
                    if y > 0:
                        if self.grid_is_marked(y-1, x) : neighbours.append(N)
                    if y < self.height - 1:
                        if self.grid_is_marked(y+1, x) : neighbours.append(S)
                    if x > 0:
                        if self.grid_is_marked(y, x-1) : neighbours.append(W)
                    if x < self.width - 1:
                        if self.grid_is_marked(y, x+1) : neighbours.append(E)

                    if neighbours != []:
                        direction = neighbours[random.randint(0, len(neighbours) - 1)]
                        nx, ny = (x + self.move_x[direction]), (y + self.move_y[direction])
                        self.add_direction_to_grid(y, x, direction)
                        self.add_direction_to_grid(ny, nx, self.opposite[direction])
                        self.mark_a_line(y, False)
                        return (x, y, empty_rows)
            if full_cells == self.width:
                empty_rows += 1
            self.mark_a_line(y, False)
                
            
        return None, None, empty_rows

    def mark_a_line(self, y, bool_val):
        for x in range(self.width):
            self.mark_grid(y, x, bool_val)

if __name__ == "__main__":
    maze = HuntAndKillAlgorithm(25, 25)
    maze.fill_maze()