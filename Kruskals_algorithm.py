import random, sys, time


FPS = 0
width = 40
height = 20
seed = 10
# random.seed(10)

class Tree:
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

N,S,W,E = 1,2,4,8
MOVE_X_DIRECTION = {N : 0, S : 0, W : -1, E : 1}
MOVE_Y_DIRECTION = {N : -1, S : 1, W : 0, E : 0}
OPPOSITE_DIRECTION = {N : S, S : N, W : E, E : W}

maze_grid = [[0]*width for i in range(height)]
path_grid = [[False]*width for i in range(height)]
sets = []
for y in range(height):
    row = []
    for x in range(width):
        row.append(Tree())
    sets.append(row)

def print_grid(grid, path_grid):
    maze_str = ""
    # ╔════════════════════════════╗
    # ║    TOP LINE OF THE MAZE    ║
    # ╚════════════════════════════╝
    maze_str += u'\u2554' # ╔ ; top left corner
    for x in range(width-1):  # width -1 because the right corner will always be "═══╗"
        maze_str += u'\u2550'*3
        # If the path is going south print "╦" else print "═"
        maze_str += u'\u2566' if ((grid[0][x] & S != 0 and grid[0][x] & E == 0) or (grid[0][x] == 0)) else u'\u2550'
    maze_str += u'\u2550'*3 + u'\u2557' + "\n" # "═══╗"
    # ╔════════════════════════════╗
    # ║     REST OF THE MAZE       ║
    # ╚════════════════════════════╝
    for y in range(height):
        # ╔════════════════════════════╗
        # ║    LEFT LINE OF THE MAZE   ║
        # ╚════════════════════════════╝
        # first_line is the middle line of the box where grid[y][x] is  [2x4]
        # second line is the lower line of the box where grid[y][x] is
        first_line = u'\u2551' # "║", it is always this
        if y == height - 1:
            second_line = u'\u255a' # "╚" for the left down corner
        else:
            second_line = u'\u2560' if (grid[y][0] & E != 0 and grid[y][0] & S == 0) else u'\u2551' # "╠" if the block is going east and not south else "║"
        # ╔════════════════════════════╗
        # ║      REST OF THE MAZE      ║
        # ║     2  LINES EACH LOOP     ║
        # ╚════════════════════════════╝   
        for x in range(width):
            # If the recursive algorithm is still in progress then "#" Where it is marked
            path_chr = "#" if path_grid[y][x] else " "
            # If it is still in progress
            # ╔════════════════════════════╗
            # ║  FIRST LINE OF EACH SPOT   ║
            # ╚════════════════════════════╝
            if path_grid[y][x]:
                if grid[y][x] & E != 0 and grid[y][x] & W != 0:
                    first_line += path_chr*4  # "####" If it goes to the east and west
                elif grid[y][x] & (N+S) != 0 and grid[y][x] & (E+W) == 0:
                    first_line += " " + path_chr + " " + u'\u2551'  # " # ║" if it is going only north or south
                elif grid[y][x] & E != 0:
                    first_line += " " + path_chr*3  # " ###" if it is only going east
                else:
                    first_line += path_chr*2 + " " + u'\u2551'  # "## ║" If it is going south and west
            else:
                # If the maze is complete in that spot of the grid
                first_line += path_chr*3 + u'\u2551' if (grid[y][x] & E == 0) else path_chr*4 # "   ║" if it is not going east else "    "
            # ╔════════════════════════════╗ 
            # ║  SECOND LINE OF EACH SPOT  ║
            # ╚════════════════════════════╝
            # For grid numbers 0, 1, 4 and 5(N and W)
            if grid[y][x] & (S+E) == 0:
                try:
                    if (grid[y][x+1] & S == 0 and grid[y+1][x] & E == 0): # if y + 1 in maze is not going east and x +1 not going south
                        second_line += u'\u2550'*3 + u'\u256c' # "═══╬"
                    elif (grid[y][x+1] & S == 0 and grid[y+1][x] & E != 0): # y+1: going east, x+1: not going south
                        second_line += u'\u2550'*3 + u'\u2569' # "═══╩"
                    elif (grid[y][x+1] & S != 0 and grid[y+1][x] & E != 0): # y+1 going east and x+1 is going south
                        second_line += u'\u2550'*3 + u'\u255d' # "═══╝"
                    else:
                        raise
                except:
                    if y == height - 1 and x == width - 1:  # If it is the down left corner
                        second_line += u'\u2550'*3 + u'\u255d' # "═══╝"
                    elif y == height -1:  # If it is on the bottom line
                        second_line += u'\u2550'*3 + u'\u2569' # "═══╩"
                    else:  # If everything else fails, should be this one I hope xd
                        second_line += u'\u2550'*3 + u'\u2563' # "═══╣"
            # For grid numbers 2, 3, 6 and 7(S, N^S, S^W, S^W^N)
            elif grid[y][x] & E == 0:
                try:
                    if (grid[y][x+1] & S == 0 and grid[y+1][x] & E == 0):
                        second_line += " " + path_chr + " " + u'\u2560' # "   ╠"
                    elif (grid[y][x+1] & S == 0):
                        second_line += " " + path_chr + " " + u'\u255a' # "   ╚"
                    else:
                        raise
                except:
                    second_line += " " + path_chr + " " + u'\u2551' # "   ║"
            # For grid numbers 8, 9, 12 and 13(E, E^N, E^W, E^W^N)
            elif grid[y][x] & S == 0:
                try:
                    if grid[y+1][x] & E == 0 and grid[y][x+1] & S == 0:
                        second_line += u'\u2550'*3 + u'\u2566' # "═══╦"
                    elif grid[y+1][x] & E == 0:
                        second_line += u'\u2550'*3 + u'\u2557' # "═══╦"
                    else:
                        raise
                except:
                    second_line += u'\u2550'*4 # "════"
            # For grid numbers 10, 11, 14 and 115(E^S, E^S^N, E^W^S, E^W^S^N)
            else:
                try:
                    if grid[y+1][x] & E == 0 and grid[y][x+1] & S == 0:
                        second_line += " " + path_chr + " " + u'\u2554' # "   ╔"
                    elif grid[y+1][x] & E == 0 and grid[y][x+1] & S != 0:
                        second_line += " " + path_chr + " " + u'\u2551' # "   ║"
                    else:
                        raise
                except:
                    second_line += " " + path_chr + " " + u'\u2550' # "   ═"
        maze_str += first_line + "\n"
        maze_str += second_line + "\n"
    # CLEAR() # Clear the terminal
    # print()
    sys.stdout.write("\r" + "\n"*(51-(width*2 + 1)) + "{}".format("\n" + maze_str))
    sys.stdout.flush()
    time.sleep(FPS)

edges = []
for y in range(height):
    for x in range(width):
        if y > 0:
            edges.append([x, y, N])
        if x > 0:
            edges.append([x, y, W])

random.shuffle(edges)

print_grid(maze_grid, path_grid)
# While it is not empty
while edges:
    x, y, direction = edges.pop()
    nx, ny = x + MOVE_X_DIRECTION[direction], y + MOVE_Y_DIRECTION[direction]

    set_1, set_2 = sets[y][x], sets[ny][nx]
    if not set_1.is_connected(set_2):
        set_1.connect_trees(set_2)
        maze_grid[y][x] |= direction
        maze_grid[ny][nx] |= OPPOSITE_DIRECTION[direction]
        path_grid[y][x], path_grid[ny][nx] = True, True
        print_grid(maze_grid, path_grid)
        time.sleep(FPS)
        path_grid[y][x], path_grid[ny][nx] = False, False

print_grid(maze_grid, path_grid)
# print(maze_grid)
