from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8

class BinaryTreeAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)
        
    def fill_maze(self):
        for y in range(self.width):
            for x in range(self.height):
                self.display_maze()
                directions = []
                if y > 0:
                    directions.append(N)
                if x > 0:
                    directions.append(W)
                
                if directions != []:
                    direction = directions[random.randint(0, len(directions) - 1)]
                    nx, ny = (x + self.move_x[direction]), (y + self.move_y[direction])
                    self.add_direction_to_grid(y, x, direction)
                    self.add_direction_to_grid(ny, nx, self.opposite[direction])
                    self.set_x_and_y(y, x)
        self.display_maze()
        self.set_x_and_y(-1, -1)
        self.display_maze()

if __name__ == "__main__":
    maze = BinaryTreeAlgorithm(25, 25)
    maze.fill_maze()