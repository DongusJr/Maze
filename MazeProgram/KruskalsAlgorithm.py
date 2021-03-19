from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8

class MSTree:
    def __init__(self):
        self.__parent = None

    def set_parent(self, new_parent):
        self.__parent = new_parent

    def root(self):
        return self.__parent.root() if self.__parent else self

    def is_connected(self, other):
        return self.root() == other.root()
    
    def connect_trees(self, other):
        other.root().set_parent(self)


class KruskalsAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)
        self.sets = [[MSTree() for x in range(self.width)] for y in range(height)]
        self.edges = self._make_edges()
        self.c_y, self.c_x = -1, -1

    def _make_edges(self):
        edges = []
        for y in range(self.height):
            for x in range(self.width):
                if y > 0:
                    edges.append((x, y, N))
                if x > 0:
                    edges.append((x, y, W))
        random.shuffle(edges)
        return edges

    def fill_tree(self):
        while self.edges:
            x, y, direction = self.edges.pop()
            nx, ny = (x + self.move_x[direction]), (y + self.move_y[direction])
            self.mark_grid(y, x, True)
            self.mark_grid(ny, nx, True)

            set_1, set_2 = self.sets[y][x], self.sets[ny][nx]
            if not set_1.is_connected(set_2):
                set_1.connect_trees(set_2)
                self.add_direction_to_grid(y, x, direction)
                self.add_direction_to_grid(ny, nx, self.opposite[direction])
                self.display_maze()
            self.mark_grid(y, x, False)
            self.mark_grid(ny, nx, False)
        self.display_maze()
                

if __name__ == "__main__":
    maze = KruskalsAlgorithm(25, 25)
    maze.fill_tree()

    