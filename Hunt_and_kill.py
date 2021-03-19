import sys, random, time

width = 50
height = 25
FPS = 0
seed = 0
# random.seed(seed)

grid = [[0]*width for i in range(height)]
path_grid = [[False]*width for i in range(height)]

N,S,W,E = 1,2,4,8
MOVE_X = {N : 0, S : 0, W : -1, E : 1}
MOVE_Y = {N : -1, S : 1, W : 0, E : 0}
OPPOSITE_DIRECTION = {N : S, S : N, W : E, E : W}

def print_grid(grid, path_grid, cy = None):
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
            if cy == y : path_chr = u'▓'
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
            path_chr = "#" if path_grid[y][x] else " "
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

def walk(grid, path_grid, x, y):
    path_grid[y][x] = False
    height = len(grid)
    width = len(grid[0])
    directions = [N, S, W, E]
    random.shuffle(directions)
    for direction in directions:
        nx, ny = x + MOVE_X[direction], y + MOVE_Y[direction]
        if 0 <= nx < width and 0 <= ny < height:
            if grid[ny][nx] == 0:
                path_grid[y][x] = True
                path_grid[ny][nx] = True
                grid[y][x] |= direction
                grid[ny][nx] |= OPPOSITE_DIRECTION[direction]
                path_grid[y][x] = False            

                return (nx, ny)
    return (None, None)

def hunt(grid, path_grid, empty_rows):
    height = len(grid)
    width = len(grid[0])
    for y in range(empty_rows, height):
        print_grid(grid, path_grid, y)
        full_cells = 0
        for x, cell in enumerate(grid[y]):
            neighbours = []
            if cell != 0:
                full_cells += 1
                continue
            else:
                if y > 0:
                    if grid[y-1][x] != 0 : neighbours.append(N)
                if y < height - 1:
                    if grid[y+1][x] != 0 : neighbours.append(S)
                if x > 0:
                    if grid[y][x-1] != 0 : neighbours.append(W)
                if x < width - 1:
                    if grid[y][x+1] != 0 : neighbours.append(E)

                if neighbours != []:
                    direction = neighbours[random.randint(0, len(neighbours) - 1)]
                    nx, ny = x + MOVE_X[direction], y + MOVE_Y[direction]

                    grid[y][x] |= direction
                    grid[ny][nx] |= OPPOSITE_DIRECTION[direction]

                    return (x, y, empty_rows)
        if full_cells == width:
            empty_rows += 1
    
    return None, None, empty_rows


def main(grid, path_grid, height, width):
    x,y = random.randint(0, width - 1), random.randint(0, height - 1)
    empty_rows = 0

    while True:
        print_grid(grid, path_grid)

        x,y = walk(grid, path_grid, x, y)
        if x == None:
            # path_grid[y][x] = False
            x, y, empty_rows = hunt(grid, path_grid, empty_rows)
        if x == None:
            break

main(grid, path_grid, height, width)
print_grid(grid, path_grid)
# print(grid)