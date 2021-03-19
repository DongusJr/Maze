from MazeDraw import MazeDraw

class OutsideOfMaze(Exception):
    pass

N, S, W, E = 1, 2, 4, 8

class Maze:

    def __init__(self, height = 5, width = 5, empty_canvas = False, show_path=True):
        self.move_x = {N : 0, S : 0, W : -1, E : 1}
        self.move_y = {N : -1, S : 1, W : 0, E : 0}
        self.opposite = {N : S, S : N, W : E, E : W}
        self.height = height
        self.width = width
        self.grid = [[0]*width for _ in range(height)]
        self.path_grid = [[False]*width for _ in range(height)]
        self.foreground_grid = None
        self.c_x = 0 # Current x
        self.c_y = 0 # Current y
        self.maze_draw = MazeDraw(self, empty_canvas, show_path)

    def get_maze_str(self):
        return str(self.maze_draw)

    def __str__(self):
        return self._make_maze_str()

    def display_next_lines(self):
        self.maze_draw.display_next_lines()

    def reset_line(self, n):
        self.maze_draw.reset_line(n)

    def display_maze(self):
        self.maze_draw.display_maze()

    def display_line(self, bottom_line = False, freeze = False):
        self.maze_draw.display_line(bottom_line, freeze)

    def display_top_of_maze(self):
        self.maze_draw.display_top_of_maze()

    def set_x_and_y(self, y, x):
        self.c_y, self.c_x = y, x

    def _make_maze_str(self):
        maze_str = ""
        for y in self.grid:
            maze_str += str(y) + "\n"
        return maze_str

    def mark_grid(self, y, x, mark_bool):
        ''' Function that marks the grid at a certain x and y coordinate '''
        if self.is_in_grid(y, x):
            self.path_grid[y][x] = mark_bool
        else:
            raise OutsideOfMaze

    def mark_foreground_grid(self, y, x, mark_bool):
        if self.is_in_grid(y, x):
            self.foreground_grid[y][x] = mark_bool
        else:
            raise OutsideOfMaze

    def add_direction_to_grid(self, y, x, direction):
        ''' Adds a direction tied to a spot in the maze '''
        if self.is_in_grid(y, x):
            self.grid[y][x] |= direction
        else:
            raise OutsideOfMaze()

    def is_in_grid(self, y, x):
        ''' Function that checks if the x and y are valid for the grid '''
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def grid_is_marked(self, y, x):
        ''' Function that checks if an x and y coordinates have already been altered '''
        try:
            return False if self.grid[y][x] == 0 else True
        except:
            return False

    def get_new_coords_after_move(self, y, x, direction):
        return (x + self.move_x[direction]), (y + self.move_y[direction])

    def get_cell(self, y, x):
        return self.grid[y][x]

    def get_cell_is_on_path(self, y, x):
        return True if self.path_grid[y][x] == True else False

if __name__ == "__main__":
    maze = Maze()
    print(maze)