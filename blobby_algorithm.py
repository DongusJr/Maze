from randomdict import RandomDict
import sys, time, random

# Make set S with set A and set B
# Take a random cell from S
# check its neighbours and add it to subset

# index = y*width + x
height = 20
width = 40
FPS = 0
seed = 1
ROOM_SIZE = 4
# random.seed(seed)

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

N,S,W,E = -width, width, -1, 1
NO, DOWN, RIGHT, ALL = 0,1,2,3
MOVE_X = {N : 0, S : 0, W : -1, E : 1}
MOVE_Y = {N : -1, S : 1, W : 0, E : 0}


set_s = RandomDict()
grid = [[0]*width for i in range(height)]


for y in range(height):
    for x in range(width):
        set_s[y*width + x] = (x,y)
        if x == width-1:
            grid[y][x] |= RIGHT
        if y == height-1:
            grid[y][x] |= DOWN

# S = {A : {}, B : {}}
# S = {0: (0,0), 1 (0,1), ..., 99 : (9,9)}

# U = {A : }



def print_grid(grid, set_a_path_grid, set_b_path_grid):
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
            if set_a_path_grid[y][x]:
                path_chr = u'▓'
            elif set_b_path_grid[y][x]:
                path_chr = u'░'
            else:
                path_chr = SPACE
            first_line += path_chr*3 + VERT_WALL if grid[y][x] & RIGHT != 0 else path_chr*4
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
                        second_line += path_chr*3 + VERT_WALL_RIGHT # "   ╠"
                    elif grid[y][x+1] & DOWN != 0:
                        second_line += path_chr*3 + BOT_LEFT_CORNER # "   ╚"
                    else:
                        raise
                except:
                    second_line += path_chr*3 + VERT_WALL # "   ║"
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
                        second_line += path_chr*3 + HORZ_WALL # "   ═"
                    elif grid[y][x+1] & DOWN != 0:
                        second_line += path_chr*3 + TOP_LEFT_CORNER # "   ╔"
                    elif grid[y+1][x] & RIGHT != 0:
                        second_line += path_chr*3 + VERT_WALL # "   ║"
                    else:
                        raise
                except:
                    second_line += path_chr*4 # "    "
               


                        
        maze_str += first_line + "\n"
        maze_str += second_line + "\n"
    sys.stdout.write("\r" + "\n"*(51-(width*2 + 1)) + "{}".format("\n" + maze_str))
    time.sleep(FPS)

def blobby_recursive(grid, set_s):
    if len(set_s) < ROOM_SIZE:
        return None
    set_a_path_grid = [[False]*len(grid[0]) for i in range(len(grid))]
    set_b_path_grid = [[False]*len(grid[0]) for i in range(len(grid))]
    print_grid(grid, set_a_path_grid, set_b_path_grid)
    set_u = RandomDict()
    x_1 ,y_1 = set_s.random_value()
    del set_s[y_1*width + x_1]
    x_2, y_2 = set_s.random_value()
    del set_s[y_2*width + x_2]

    set_u["A"] = RandomDict()
    set_u["B"] = RandomDict()
    set_u["A"][y_1*width + x_1] = (x_1, y_1)
    set_u["B"][y_2*width + x_2] = (x_2, y_2)
    set_a_path_grid[y_1][x_1] = True
    set_b_path_grid[y_2][x_2] = True

    set_a = RandomDict()
    set_b = RandomDict()

    print_grid(grid, set_a_path_grid, set_b_path_grid)
    
    path_count = 0
    while set_u["A"] or set_u["B"]:
        random_set_str = "A" if random.randint(0,1) == 0 else "B"
        try:
            c_x, c_y = set_u[random_set_str].random_value()
        except:
            random_set_str = "A" if random_set_str == "B" else "B"
            c_x, c_y = set_u[random_set_str].random_value()
        del set_u[random_set_str][c_y*width + c_x]
        if random_set_str == "A":
            set_a[c_y*width + c_x] = (c_x, c_y)
        else:
            set_b[c_y*width + c_x] = (c_x, c_y)
        for direction in [N,S,E,W]:
            try:
                if set_s[(c_y*width + c_x) + direction]:
                    path_count += 1
                    nx, ny = c_x + MOVE_X[direction], c_y + MOVE_Y[direction]
                    if 0 <= nx < width and 0 <= y < height:
                        set_u[random_set_str][(c_y*width + c_x) + direction] = (nx, ny)
                        if random_set_str == "A":
                            set_a_path_grid[ny][nx] = True
                        else:
                            set_b_path_grid[ny][nx] = True
                        del set_s[(c_y*width + c_x) + direction]
                else:
                    raise
            except:
                continue

        if path_count >= 8:
            print_grid(grid, set_a_path_grid, set_b_path_grid)
            path_count = 0
    
    wall_cords = make_walls(set_a, set_b, grid)
    wall_cords += make_walls(set_b, set_a, grid)
    if len(wall_cords) > 0:
        print_grid(grid, set_a_path_grid, set_b_path_grid)
    r_x, r_y, wall_direction = random.choice(wall_cords)
    grid[r_y][r_x] ^= wall_direction
    if len(wall_cords) > 0:
        print_grid(grid, set_a_path_grid, set_b_path_grid)
    
    set_max = set_a if len(set_a) >= len(set_b) else set_b
    set_min = set_b if len(set_a) >= len(set_b) else set_a
    blobby_recursive(grid, set_a)
    blobby_recursive(grid, set_b)

def make_walls(set_to_check, set_to_observe, grid):
    wall_coords = []
    for index, coordinates in set_to_check.items():
        x,y = coordinates
        try:
            if x != width - 1:
                set_to_observe[index + E]
                grid[y][x] |= RIGHT
                wall_coords.append((x,y,RIGHT))
        except:
            pass
        try:
            if y != height - 1:
                set_to_observe[index + S]
                grid[y][x] |= DOWN
                wall_coords.append((x,y,DOWN))
        except:
            pass

    return wall_coords

while True:
    set_s = RandomDict()
    grid = [[0]*width for i in range(height)]


    for y in range(height):
        for x in range(width):
            set_s[y*width + x] = (x,y)
            if x == width-1:
                grid[y][x] |= RIGHT
            if y == height-1:
                grid[y][x] |= DOWN

    blobby_recursive(grid, set_s)
    set_a_path_grid = [[False]*len(grid[0]) for i in range(len(grid))]
    set_b_path_grid = [[False]*len(grid[0]) for i in range(len(grid))]
    print_grid(grid, set_a_path_grid, set_b_path_grid)






    
