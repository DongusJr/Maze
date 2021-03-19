import time, os, sys
from colorama import *
init()
TOP_LEFT_CORNER =  u'\u2554' # ╔
TOP_RIGHT_CORNER = u'\u2557' # ╗
BOT_LEFT_CORNER =  u'\u255a' # ╚
BOT_RIGHT_CORNER = u'\u255d' # ╝
VERT_WALL =        u'\u2551' # ║
HORZ_WALL =        u'\u2550' # ═
VERT_WALL_RIGHT =  u'\u2560' # ╠
VERT_WALL_LEFT =   u'\u2563' # ╣
HORZ_WALL_UP =     u'\u2569' # ╩
HORZ_WALL_DOWN =   u'\u2566' # ╦
WALL_ALL =         u'\u256c' # ╬
SPACE =            " "


N,S,W,E = 1, 2, 4, 8
EMPTY, DOWN, RIGHT, FULL = 0,1,2,3 # For empty canvas





class MazeDraw:
    def __init__(self, maze, empty_canvas = False, show_path = True):
        self.maze = maze
        self.fps = 0
        self.width = maze.width
        self.height = maze.height
        self.empty_canvas = empty_canvas
        self.path_chr = " " if not show_path else u'░'
        self.fore_chr = " " if not show_path else u'▒'

    def reset_line(self, n):
        for i in range(n):
            sys.stdout.write("\u001b[1A")
            sys.stdout.write("\u001b[1000D")
            sys.stdout.write("\u001b[0K")
            sys.stdout.write("\u001b[1000D")

    def display_next_lines(self):
        self.display_line()

    def display_maze(self):
        maze_str = str(self)
        sys.stdout.write("\r" + "\n"*(51-(self.width*2 + 1)) + "{}".format("\n" + maze_str))
        time.sleep(self.fps)

    def display_line(self, bottom_line = False, freeze = False):
        y = 1 if bottom_line else 0
        maze_str = ""
        maze_str += self._draw_first_line_left_side()
        maze_str += self._draw_first_line_right_side(y)
        if bottom_line:
            maze_str += self._draw_bottom_grid_for_line()
        else:
            maze_str += self._draw_second_line_left_side(y)
            maze_str += self._draw_second_line_right_side(y)
        sys.stdout.write("{}".format(maze_str))
        if freeze:
            time.sleep(self.fps)

    def display_top_of_maze(self):
        sys.stdout.write(self._draw_top_line_of_maze())

    def __str__(self):
        maze_str = ""
        maze_str += self._draw_top_line_of_maze()
        if self.empty_canvas:
            for y in range(self.height):
                maze_str += self._draw_first_line_left_side()
                maze_str += self._draw_first_line_right_side_empty_canvas(y)
                maze_str += self._draw_second_line_left_side(y)
                maze_str += self._draw_second_line_right_side_empty_canvas(y)
        else:
            for y in range(self.height):
                maze_str += self._draw_first_line_left_side()
                maze_str += self._draw_first_line_right_side(y)
                maze_str += self._draw_second_line_left_side(y)
                maze_str += self._draw_second_line_right_side(y)
        return maze_str

    def _draw_second_line_right_side_empty_canvas(self, y):
        second_line = ""
        for x in range(self.width):
            if self.is_on_current(y,x):
                path = u'▓'
            elif self.is_on_foreground(y, x):
                path = self.fore_chr
            else:
                path = self.path_chr if self.is_on_path(y, x) else SPACE

            if self.maze.grid[y][x] == (RIGHT + DOWN):
                second_line += HORZ_WALL*3
                try:
                    if self.contains(y+1, x, RIGHT) and self.contains(y, x+1, DOWN):
                        second_line += WALL_ALL
                    elif self.contains(y+1, x, RIGHT):
                        second_line += VERT_WALL_LEFT
                    elif self.contains(y, x+1, DOWN):
                        second_line += HORZ_WALL_UP
                    else:
                        raise
                except:
                    if y != self.height - 1 and x == self.width - 1:
                        second_line += VERT_WALL_LEFT
                    elif y == self.height - 1 and x != self.width - 1:
                        second_line += HORZ_WALL_UP
                    else:
                        second_line += BOT_RIGHT_CORNER
            elif self.maze.grid[y][x] == RIGHT:
                second_line += path*3
                try:
                    if self.contains(y+1, x, RIGHT) and self.contains(y, x+1, DOWN):
                        second_line += VERT_WALL_RIGHT
                    elif self.contains(y, x+1, DOWN):
                        second_line += BOT_LEFT_CORNER
                    else:
                        raise
                except:
                    second_line += VERT_WALL
            elif self.maze.grid[y][x] == DOWN:
                second_line += HORZ_WALL*3
                try:
                    if self.contains(y+1, x, RIGHT) and self.contains(y, x+1, DOWN):
                        second_line += HORZ_WALL_DOWN
                    elif self.contains(y+1, x, RIGHT):
                        second_line += TOP_RIGHT_CORNER
                    else:
                        raise
                except:
                    second_line += HORZ_WALL
            else:
                second_line += path*3
                try:
                    if self.contains(y, x+1, DOWN) and self.not_contains(y+1, x, RIGHT):
                        second_line += HORZ_WALL
                    elif self.contains(y, x+1, DOWN):
                        second_line += TOP_LEFT_CORNER
                    elif self.contains(y+1, x, RIGHT):
                        second_line += VERT_WALL
                    else:
                        raise
                except:
                    second_line += path
        return second_line + "\n"


    def _draw_first_line_right_side_empty_canvas(self, y):
        first_line = ""
        for x in range(self.width):
            if self.is_on_current(y,x):
                path = u'▓'
            elif self.is_on_foreground(y, x):
                path = self.fore_chr
            else:
                path = self.path_chr if self.is_on_path(y, x) else SPACE

            first_line += path*3 + VERT_WALL if self.contains(y, x, RIGHT) else path*4
        return first_line + "\n"

    def _draw_bottom_grid_for_line(self):
        second_line = BOT_LEFT_CORNER
        for x in range(self.width):
            if x == self.width - 1:
                second_line += HORZ_WALL*3 + BOT_RIGHT_CORNER
            elif self.not_contains(1, x, E):
                second_line += HORZ_WALL*3 + HORZ_WALL_UP
            else:
                second_line += HORZ_WALL*4
        return second_line + "\n"


    def add_closed_grid(self, y, x):
        second_line = HORZ_WALL*3
        try:
            if self.not_contains(y, x+1, S) and self.not_contains(y+1, x, E):
                second_line += WALL_ALL
            elif self.not_contains(y, x+1, S) and self.contains(y+1, x, E):
                second_line += HORZ_WALL_UP
            elif self.contains(y, x+1, S) and self.contains(y+1, x, E):
                second_line += BOT_RIGHT_CORNER
            else:
                raise
        except:
            if self.is_bottom_y(y) and self.is_bottom_x(x):
                second_line += BOT_RIGHT_CORNER
            elif self.is_bottom_y(y):
                second_line += HORZ_WALL_UP
            else:
                second_line += VERT_WALL_LEFT
        return second_line

    def add_open_south_grid(self, y, x, path):
        second_line = SPACE + path + SPACE
        try:
            if self.not_contains(y, x+1, S) and self.not_contains(y+1, x, E):
                second_line += VERT_WALL_RIGHT
            elif self.not_contains(y, x+1, S):
                second_line += BOT_LEFT_CORNER
            else:
                raise
        except:
            second_line += VERT_WALL
        return second_line
            
    def add_open_east_grid(self, y, x):
        second_line = HORZ_WALL*3
        try:
            if self.not_contains(y+1, x, E) and self.not_contains(y, x+1, S):
                second_line += HORZ_WALL_DOWN
            elif self.not_contains(y+1, x, E):
                second_line += TOP_RIGHT_CORNER
            else:
                raise
        except:
            second_line += HORZ_WALL
        return second_line

    def add_open_grid(self, y, x, path):
        second_line = SPACE + path + SPACE
        try:
            if self.not_contains(y+1, x, E) and self.contains(y, x+1, S):
                second_line += VERT_WALL
            elif self.not_contains(y+1, x, E) and self.not_contains(y, x+1, S):
                second_line += TOP_LEFT_CORNER
            else:
                raise
        except:
            second_line += HORZ_WALL
        return second_line

    def _draw_second_line_right_side(self, y):
        second_line = ""
        for x in range(self.width):
            if self.is_on_current(y, x):
                path = u'▓'
            elif self.is_on_foreground(y, x):
                path = self.fore_chr
            else:
                path = self.path_chr if self.is_on_path(y,x) else SPACE

            if self.not_contains(y, x, S+E):
                second_line += self.add_closed_grid(y,x)
            elif self.not_contains(y ,x ,E):
                second_line += self.add_open_south_grid(y, x, path)
            elif self.not_contains(y, x, S):
                second_line += self.add_open_east_grid(y, x)
            else:
                second_line += self.add_open_grid(y, x, path)
        return second_line + "\n"

    def _draw_second_line_left_side(self, y):
        if y == self.height - 1:
            return BOT_LEFT_CORNER
        else:
            if self.empty_canvas:
                return VERT_WALL_RIGHT if self.contains(y, 0, DOWN) else VERT_WALL
            else:
                return VERT_WALL_RIGHT if self.not_contains(y, 0, S) else VERT_WALL

    def _draw_first_line_left_side(self):
        return VERT_WALL

    def add_first_line_not_on_path(self, y, x, path):
        return SPACE + path + SPACE  + VERT_WALL if (self.not_contains(y,x,E)) else path*4

    def _draw_first_line_right_side(self, y):
        first_line = ""
        for x in range(self.width):
            if self.is_on_current(y,x):
                path = u'▓'
            elif self.is_on_foreground(y, x):
                path = self.fore_chr
            else:
                path = self.path_chr if self.is_on_path(y, x) else SPACE
            if self.is_on_path(y, x):
                if self.contains(y, x, E) and self.contains(y, x, W):
                    first_line += path*4
                elif self.contains(y, x, N+S) and self.not_contains(y, x, E+W):
                    first_line += SPACE + path + SPACE + VERT_WALL
                elif self.contains(y, x, E):
                    first_line += SPACE + path*3
                else:
                    first_line += path*2 + SPACE + VERT_WALL
            else:
                first_line += self.add_first_line_not_on_path(y, x, path)
        return first_line + "\n"

    def _draw_top_line_of_maze(self):
        top_line = TOP_LEFT_CORNER
        for x in range(self.width - 1):
            top_line += HORZ_WALL*3
            if self.empty_canvas:
                top_line += HORZ_WALL_DOWN if self.contains(0, x, RIGHT) else HORZ_WALL
            else: 
                top_line += HORZ_WALL_DOWN if self.not_contains(0, x, E) else HORZ_WALL
        top_line += HORZ_WALL*3 + TOP_RIGHT_CORNER
        return top_line + "\n"
        
    def is_zero(self, y, x):
        return True if self.maze.grid[y][x] == 0 else False

    def contains(self, y, x, direction):
        if self.maze.get_cell(y, x) & direction != 0:
            return True
        return False

    def not_contains(self, y, x, direction):
        if self.maze.get_cell(y, x) & direction == 0:
            return True
        return False

    def is_empty(self, y, x):
        if not self.maze.grid_is_marked(y, x):
            return True
        return False

    def is_bottom_y(self, y):
        return True if y == self.height - 1 else False

    def is_bottom_x(self, x):
        return True if x == self.width - 1 else False

    def is_on_path(self, y, x):
        return True if self.maze.get_cell_is_on_path(y, x) else False

    def is_on_current(self, y, x):
        return True if self.maze.c_x == x and self.maze.c_y == y else False

    def is_on_foreground(self, y, x):
        try:
            return True if self.maze.foreground_grid[y][x] == True else False
        except:
            return False