from Maze import Maze
from randomdict import RandomDict
import random
# random.seed(2)

EMPTY, DOWN, RIGHT, FULL = 0, 1, 2, 3
HORIZONTAL = 1
VERTICAL = 2

class BlobbyAlgorithm(Maze):
    
    def __init__(self, height=5, width=5, room_size = 4):
        super().__init__(height, width, True, False)    
        self.n, self.s, self.w, self.e = -width, width, -1, 1
        self.room_size = room_size
        self.foreground_grid = [[False]*width for _ in range(height)]
        self.set_s = RandomDict()
        self.c_x, self.c_y = -1, -1
        for y in range(height):
            for x in range(width):
                self.set_s[y*width + x] = (x,y)
                if x == width-1:
                    self.grid[y][x] |= RIGHT
                if y == height-1:
                    self.grid[y][x] |= DOWN
        self.move_x = {self.n : 0, self.s : 0, self.w : -1, self.e : 1}
        self.move_y = {self.n : -1, self.s : 1, self.w : 0, self.e : 0}

    def fill_maze(self):
        self.blobby_recursive(self.set_s)
        self.foreground_grid = [[False]*self.width for _ in range(self.height)]
        self.path_grid = [[False]*self.width for _ in range(self.height)]
        self.display_maze()

    def blobby_recursive(self, set_s):
        if len(set_s) < self.room_size:
            return None
        self.foreground_grid = [[False]*self.width for _ in range(self.height)]
        self.path_grid = [[False]*self.width for _ in range(self.height)]
        self.display_maze()
        set_u = RandomDict()
        x_1, y_1 = set_s.random_value()
        del set_s[y_1*self.width + x_1]
        x_2, y_2 = set_s.random_value()
        del set_s[y_2*self.width + x_2]
        set_u["A"] = RandomDict()
        set_u["B"] = RandomDict()
        set_u["A"][y_1*self.width + x_1] = (x_1, y_1)
        set_u["B"][y_2*self.width + x_2] = (x_2, y_2)
        self.mark_grid(y_1, x_1, True)
        self.mark_foreground_grid(y_2, x_2, True)

        set_a = RandomDict()
        set_b = RandomDict()

        self.display_maze()

        path_count = 0
        while set_u["A"] or set_u["B"]:
            random_set_str = "A" if random.randint(0,1) == 0 else "B"
            try:
                c_x, c_y = set_u[random_set_str].random_value()
            except:
                random_set_str = "A" if random_set_str == "B" else "B"
                c_x, c_y = set_u[random_set_str].random_value()
            del set_u[random_set_str][c_y*self.width + c_x]
            if random_set_str == "A":
                set_a[c_y*self.width + c_x] = (c_x, c_y)
            else:
                set_b[c_y*self.width + c_x] = (c_x, c_y)
            for direction in [self.n, self.s, self.e, self.w]:
                try:
                    if set_s[(c_y*self.width + c_x) + direction]:
                        path_count += 1
                        nx, ny = (c_x + self.move_x[direction]), (c_y + self.move_y[direction])
                        if self.is_in_grid(ny, nx):
                            set_u[random_set_str][(c_y*self.width + c_x) + direction] = (nx, ny)
                            if random_set_str == "A":
                                self.mark_grid(ny, nx, True)
                            else:
                                self.mark_foreground_grid(ny, nx, True)
                            del set_s[(c_y*self.width + c_x) + direction]
                    else:
                        raise
                except:
                    continue
            if path_count >= 8:
                self.display_maze()
                path_count = 0
    
        wall_coords = self.make_walls(set_a, set_b)
        wall_coords += self.make_walls(set_b, set_a)
        if len(wall_coords) > 0:
            self.display_maze()
        r_x, r_y, wall_direction = random.choice(wall_coords)
        self.grid[r_y][r_x] ^= wall_direction
        if len(wall_coords) > 0:
            self.display_maze()
        
        set_max = set_a if len(set_a) >= len(set_b) else set_b
        set_min = set_b if len(set_a) >= len(set_b) else set_a
        self.blobby_recursive(set_max)
        self.blobby_recursive(set_min)

    
    def make_walls(self, set_to_check, set_to_observe):
        wall_coords = []
        for index, coordinates in set_to_check.items():
            x,y = coordinates
            try:
                if x != self.width - 1:
                    set_to_observe[index + self.e]
                    self.grid[y][x] |= RIGHT
                    wall_coords.append((x,y,RIGHT))
            except:
                pass
            try:
                if y != self.height - 1:
                    set_to_observe[index + self.s]
                    self.grid[y][x] |= DOWN
                    wall_coords.append((x,y,DOWN))
            except:
                pass
        return wall_coords


if __name__ == "__main__":
    maze = BlobbyAlgorithm(25, 50)
    maze.fill_maze()