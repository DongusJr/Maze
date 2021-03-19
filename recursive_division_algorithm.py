import random, sys, time

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
width = 40
height = 20

EMPTY, DOWN, RIGHT, FULL = 0,1,2,3
HORIZONTAL = 1
VERTICAL = 2
# random.seed(10)

grid = [[0]*width for i in range(height)]
for i in range(height):
    grid[i][-1] |= 2
for i in range(width):
    grid[-1][i] |= 1
FPS = 0.05 

def print_grid(grid):
    height, width = len(grid), len(grid[0])
    maze_str = ""
    maze_str += TOP_LEFT_CORNER # ╔ Always first
    for x in range(width - 1):
        # ═══╦ if there is a vertical wall below it else ════ 
        maze_str += HORZ_WALL*3 + HORZ_WALL_DOWN if grid[0][x] & RIGHT != 0 else HORZ_WALL*4 
    maze_str += HORZ_WALL*3 + TOP_RIGHT_CORNER + "\n" # ═══╗ # Always last
    for y in range(height):
        first_line = VERT_WALL # ║, Always like this
        second_line = VERT_WALL_RIGHT if grid[y][0] & DOWN != 0 else VERT_WALL
        if y == height - 1:
            second_line = BOT_LEFT_CORNER # ╚, if we reach the end
        for x in range(width):
            # "   ║" if there needs to be a wall else "    "
            first_line += SPACE*3 + VERT_WALL if grid[y][x] & RIGHT != 0 else SPACE*4
            if grid[y][x] == (RIGHT + DOWN):
                # ═══╝ | ═══╣ |═══╬ | ═══╩
                try:
                    if grid[y+1][x] & RIGHT != 0 and grid[y][x+1] & DOWN != 0:
                        second_line += HORZ_WALL*3 + WALL_ALL # ═══╬
                    elif grid[y+1][x] & RIGHT != 0:
                        second_line += HORZ_WALL*3 + VERT_WALL_LEFT # ═══╣
                    elif grid[y][x+1] & DOWN != 0:
                        second_line += HORZ_WALL*3 + HORZ_WALL_UP # ═══╩
                    else:
                        raise
                except:
                    if y != height - 1 and x == width - 1:
                        second_line += HORZ_WALL*3 + VERT_WALL_LEFT # ═══╣
                    elif y == height -1 and x != width - 1:
                        second_line += HORZ_WALL*3 + HORZ_WALL_UP # ═══╩
                    else:
                        second_line += HORZ_WALL*3 + BOT_RIGHT_CORNER # ═══╝

            elif grid[y][x] == RIGHT:
                # "   ║" | "   ╚" | "   ╠"
                try:
                    if grid[y+1][x] & RIGHT != 0 and grid[y][x+1] & DOWN != 0:
                        second_line += SPACE*3 + VERT_WALL_RIGHT # "   ╠"
                    elif grid[y][x+1] & DOWN != 0:
                        second_line += SPACE*3 + BOT_LEFT_CORNER # "   ╚"
                    else:
                        raise
                except:
                    second_line += SPACE*3 + VERT_WALL # "   ║"
            elif grid[y][x] == DOWN:
                # ════ | ═══╗ | ═══╦
                try:
                    if grid[y+1][x] & RIGHT != 0 and grid[y][x+1] & DOWN != 0:
                        second_line += HORZ_WALL*3 + HORZ_WALL_DOWN # ═══╦
                    elif grid[y+1][x] & RIGHT != 0:
                        second_line += HORZ_WALL*3 + TOP_RIGHT_CORNER # ═══╗
                    else:
                        raise
                except:
                    second_line += HORZ_WALL*4 # ════

            else:
                # "   ║" | "   ╔" | "   ═"
                try:
                    if grid[y][x+1] & DOWN != 0 and grid[y+1][x] & RIGHT == 0:
                        second_line += SPACE*3 + HORZ_WALL # "   ═"
                    elif grid[y][x+1] & DOWN != 0:
                        second_line += SPACE*3 + TOP_LEFT_CORNER # "   ╔"
                    elif grid[y+1][x] & RIGHT != 0:
                        second_line += SPACE*3 + VERT_WALL # "   ║"
                    else:
                        raise
                except:
                    second_line += SPACE*4 # "    "
               


                        
        maze_str += first_line + "\n"
        maze_str += second_line + "\n"
    sys.stdout.write("\r" + "\n"*(51-(width*2 + 1)) + "{}".format("\n" + maze_str))
    time.sleep(FPS)

def choose_orientation(width, height):
    if width < height:
        return HORIZONTAL
    elif height < width:
        return VERTICAL
    else:
        return HORIZONTAL if random.randint(0,1) == 0 else VERTICAL

def divide(grid, x, y, width, height, orientation):
    if width < 2 or height < 2:
        return None

    
    go_horizontal = orientation == HORIZONTAL
    # Wall
    wx = x + (0 if go_horizontal else random.randint(0, width - 2))
    wy = y + (random.randint(0, height - 2) if go_horizontal else 0)

    # Passage
    px = wx + (random.randint(0, width - 2) if go_horizontal else 0)
    py = wy + (0 if go_horizontal else random.randint(0, height - 2))

    dx = 1 if go_horizontal else 0
    dy = 0 if go_horizontal else 1

    length = width if go_horizontal else height

    # Perpendicular
    direction = DOWN if go_horizontal else RIGHT

    for i in range(length):
        grid[wy][wx] |= direction
        wx += dx
        wy += dy

    print_grid(grid)
    grid[py][px] = grid[py][px] ^ direction
    print_grid(grid)

    nx, ny = x, y
    w, h = [width, wy - y + 1] if go_horizontal else [wx - x + 1, height]
    divide(grid, nx, ny, w, h, choose_orientation(w, h))

    nx, ny = [x, wy + 1] if go_horizontal else [wx + 1, y]
    w, h = [width, y + height - wy - 1] if go_horizontal else [x + width - wx - 1, height]
    divide(grid, nx, ny, w, h, choose_orientation(w, h))

print_grid(grid)
time.sleep(2)
divide(grid, 0, 0, width, height, choose_orientation(width, height))
print_grid(grid)
# for i in range(height):
#     print(grid[i])
