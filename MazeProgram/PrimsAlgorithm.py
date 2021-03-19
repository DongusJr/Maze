from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8
IN = 16
FRONTIER = 32

class PrimsAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)
        self.frontiers = []
        self.c_y, self.c_x = -1, -1

    def fill_maze(self):
        self.mark_cell(random.randint(0, self.height-1), random.randint(0, self.width - 1))
        while self.frontiers:
            x, y = self.frontiers.pop(random.randint(0, len(self.frontiers) - 1))
            neighbour_list = self.neighbours(y,x)
            nx, ny = neighbour_list[random.randint(0, len(neighbour_list) - 1)]

            direction = self.get_direction(x, y, nx, ny)
            self.add_direction_to_grid(y, x, direction)
            self.add_direction_to_grid(ny, nx, self.opposite[direction])
            self.mark_grid(y, x, True)
            self.mark_grid(ny, nx, True)

            self.mark_cell(y, x)
            self.display_maze()
            self.mark_grid(y, x, False)
            self.mark_grid(ny, nx, False)
        self.display_maze()

    def add_frontier(self, y, x):
        if self.is_in_grid(y, x) and not self.grid_is_marked(y, x):
            self.add_direction_to_grid(y, x, FRONTIER)
            self.frontiers.append((x,y))

    def mark_cell(self, y, x):
        self.add_direction_to_grid(y, x, IN)
        self.add_frontier(y, x+1)
        self.add_frontier(y, x-1)
        self.add_frontier(y+1, x)
        self.add_frontier(y-1, x)

    def neighbours(self, y, x):
        n = []
        if x > 0:
            if self.contains(y, x-1, IN):
                n.append((x-1, y))
        if x < self.width - 1:
            if self.contains(y, x+1, IN):
                n.append((x+1, y))
        if y > 0:
            if self.contains(y-1, x, IN):
                n.append((x, y-1))
        if y < self.height - 1:
            if self.contains(y+1, x, IN):
                n.append((x, y+1))

        return n

    def get_direction(self, from_x, from_y, to_x, to_y):
        if from_x < to_x:
            return E
        elif from_x > to_x:
            return W
        elif from_y < to_y:
            return S
        else:
            return N

    def contains(self, y, x, direction):
        if self.get_cell(y, x) & direction != 0:
            return True
        return False

if __name__ == "__main__":
    maze = PrimsAlgorithm(25, 25)
    maze.fill_maze()