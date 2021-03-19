import random, sys, time

N, S, E, W = 1, 2, 4, 8
IN = 16
FRONTIER = 32

FPS = 0
height = 20
width = 40
seed = 10
# random.seed(seed)

grid = [[0]*width for i in range(height)]
path_grid = [[False]*width for i in range(width)]
frontiers = []
OPPOSITE_DIRECTION = {N : S, S : N, W : E, E : W}

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
    # sys.stdout.flush()
    time.sleep(FPS)

def add_frontier(x, y, grid, frontiers):
    if x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid):
        if grid[y][x] == 0:
            grid[y][x] |= FRONTIER
            frontiers.append([x,y])

def mark_cell(x, y, grid, frontiers):
    grid[y][x] |= IN
    add_frontier(x+1, y, grid, frontiers)
    add_frontier(x-1, y, grid, frontiers)
    add_frontier(x, y+1, grid, frontiers)
    add_frontier(x, y-1, grid, frontiers)

def neighbours(x, y, grid):
    n = []
    if x > 0:
        if grid[y][x-1] & IN != 0:
            n.append([x-1, y])
    if x+1 < len(grid[0]):
        if grid[y][x+1] & IN != 0:
            n.append([x+1, y])
    if y > 0:
        if grid[y-1][x] & IN != 0:
            n.append([x, y-1])
    if y+1 < len(grid):
        if grid[y+1][x] & IN != 0:
            n.append([x, y+1])

    return n

def get_direction(from_x, from_y, to_x, to_y):
    if from_x < to_x:
        return E
    elif from_x > to_x:
        return W
    elif from_y < to_y:
        return S
    else:
        return N

mark_cell(random.randint(0, width - 1,), random.randint(0, height - 1), grid, frontiers)
while frontiers:
    x, y = frontiers.pop(random.randint(0, len(frontiers) - 1))
    neighbour_list = neighbours(x,y, grid)
    nx, ny = neighbour_list[random.randint(0, len(neighbour_list) - 1)]

    direction = get_direction(x, y, nx, ny)
    grid[y][x] |= direction
    grid[ny][nx] |= OPPOSITE_DIRECTION[direction]
    path_grid[y][x], path_grid[ny][nx] = True, True

    mark_cell(x, y, grid, frontiers)
    print_grid(grid, path_grid)
    path_grid[y][x], path_grid[ny][nx] = False, False

print_grid(grid, path_grid)


    
