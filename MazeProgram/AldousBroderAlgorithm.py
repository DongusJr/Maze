from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8

class AldousBroderAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)
        self.c_x = random.randint(0, self.width - 1)
        self.c_y = random.randint(0, self.height - 1)
        self.remaining = self.width*self.height - 1

    def fill_maze(self):
        self.display_maze()
        while self.remaining > 0:
            direction = random.choice([N, S, W, E])
            n_x, n_y = (self.c_x + self.move_x[direction]), (self.c_y + self.move_y[direction])
            if self.is_in_grid(n_y, n_x):
                # self.mark_grid(self.c_y, self.c_x, False)
                # self.mark_grid(n_y, n_x, True)
                if not self.grid_is_marked(n_y, n_x):
                    self.add_direction_to_grid(self.c_y, self.c_x, direction)
                    self.add_direction_to_grid(n_y, n_x, self.opposite[direction])
                    self.remaining -= 1
                self.set_x_and_y(n_y, n_x)
                self.display_maze()
        self.set_x_and_y(-1, -1)
        self.display_maze()
                

if __name__ == "__main__":
    maze = AldousBroderAlgorithm(25, 25)
    maze.fill_maze()
