from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8

class SidewinderAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)

    def fill_maze(self):
        for y in range(self.height):
            run_start = 0
            for x in range(self.width):
                if y > 0 and (x == self.width - 1 or random.randint(0, 1) == 0):
                    cell = run_start + random.randint(0, x - run_start)
                    self.add_direction_to_grid(y, cell, N)
                    self.add_direction_to_grid(y-1, cell, S)
                    self.set_x_and_y(y,cell)
                    self.display_maze()
                    run_start = x + 1
                elif x < self.width - 1:
                    self.add_direction_to_grid(y, x, E)
                    self.add_direction_to_grid(y, x+1, W)
                    self.set_x_and_y(y,x)
                    self.display_maze()
        self.set_x_and_y(-1, -1)
        self.display_maze()
        

if __name__ == "__main__":
    maze = SidewinderAlgorithm(25, 25)
    maze.fill_maze()

