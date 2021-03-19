# RandomDict() makes for quick random values in dict, O(1)
from randomdict import RandomDict
import sys, time, random

height = 25
width = 25
FPS = 0
seed = 10
# random.seed(seed)

N,S,W,E = 1,2,4,8
IN = 16
MOVE_X = {N : 0, S : 0, W : -1, E : 1}
MOVE_Y = {N : -1, S : 1, W : 0, E : 0}
OPPOSITE_DIRECTION = {N : S, S : N, W : E, E : W}

available_cells = RandomDict()
grid = [[0]*width for i in range(height)]
path_grid = [[False]*width for i in range(height)]

k = 0
for y in range(height):
    for x in range(width):
        available_cells[k] = (y,x)   # Can locate cells by using available_cells[y*width + x]
        k += 1

def print_grid(grid, path_grid, checked_cells = None):
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
            path_chr = u'▓' if path_grid[y][x] else " "
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
                try:
                    if checked_cells[y][x]:
                        empty_chr = "X"
                    else:
                        raise
                except:
                    if grid[y][x] == 0:
                        empty_chr = "#"
                    else:
                        empty_chr = " "
                first_line += path_chr + empty_chr + path_chr + u'\u2551' if (grid[y][x] & E == 0) else path_chr*4 # "   ║" if it is not going east else "    "
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
    # sys.stdout.flush()
    time.sleep(FPS)

def walk(grid, available_cells, path_grid):
    width = len(grid[0])
    height = len(grid)
    checked_cells = [[False]*width for i in range(height)]
    cy, cx = available_cells.random_value()

    visits = {(cx, cy) : 0}

    start_x, start_y = cx, cy
    walking = True
    directions = [N, S, W, E]
    while walking:
        walking = False
        random.shuffle(directions)
        for direction in directions:
            nx, ny = cx + MOVE_X[direction], cy + MOVE_Y[direction]
            if 0 <= nx < width and 0 <= ny < height:
                visits[(cx, cy)] = direction
                path_grid[cy][cx] = True
                checked_cells[cy][cx] = True
                print_grid(grid, path_grid, checked_cells)
                path_grid[cy][cx] = False
                if grid[ny][nx] != 0:
                    break
                else:
                    cx, cy = nx, ny
                    walking = True
                    break
    
    path = []
    x, y = start_x, start_y
    while True:
        try:
            direction = visits[(x,y)]
        except:
            break
        del available_cells[y*width + x]
        path.append([x,y,direction])
        x,y = x + MOVE_X[direction], y + MOVE_Y[direction]
    return path


def main(grid, path_grid, available_cells, width, height):
    y,x = available_cells.random_value()
    del available_cells[y*width + x] # The chosen x,y coordinates are no longer available for the walk
    grid[y][x] = IN

    remaining = width * height - 1

    while remaining > 0:
        for x,y,direction in walk(grid, available_cells, path_grid):
            nx, ny = x + MOVE_X[direction], y + MOVE_Y[direction]

            grid[y][x] |= direction
            grid[ny][nx] |= OPPOSITE_DIRECTION[direction]

            path_grid[y][x] = True
            print_grid(grid, path_grid)
            path_grid[y][x] = False

            remaining -= 1

main(grid, path_grid, available_cells, width, height)
print_grid(grid, path_grid)

