import time, sys, random


width = 50
height = 25
FPS = 0
seed = 10
random.seed(seed)

N,S,E,W = 1,2,4,8
MOVE_X = {N: 0, S: 0, W: -1, E: 1}
MOVE_Y = {N: -1, S: 1, W: 0, E: 0}
OPPOSITE_DIRECTION = {N: S, S: N, W: E, E: W}

grid = [[0]*width for i in range(height)]
path_grid = [[False]*width for i in range(height)]
pos_index = None

request_text = " What kind of maze do you want? "

print(u'╔' + u'═'*len(request_text) + u'╗' + "\n" + \
      u'║' + request_text + u'║' + "\n" + \
      u'╚' + u'═'*(len(request_text)) + u'╝')

mode_str = input()


class Mode:
    ''' Class that parses text into how the growing_tree_algorithm behaves

        get an input on the form:
        1 : "{name}"
        2 : ("{name}:{weight}" + ","?)*
        3 : ("({name}" + ","?)* + ";"?)*

        NAME
        ----------------------------------------------------------------------------------
        * each time the algorithm goes to a dead end it will for these name *
        oldest - go to the original coordinates
        newest - go to the coordinates where it came from previously
        middle - go to the coordinates that are in the middle of the path that the algorithm has passed
        random - go to a random coordinate it has already passed
        ----------------------------------------------------------------------------------
        SYNTAX
        ----------------------------------------------------------------------------------------------------------------
        * What syntax is possible to use to change the algorithm in a fun way *
        ":" - indicates the weight of a name, in other words how likely(in procent) it will go following that names rule
        ";" - Indicates order of the name sequence, works like a queue
        "," - Indicates a split so that every name in the split has an equal likeness to be picked
        ----------------------------------------------------------------------------------------------------------------
        EXAMPLES
        ----------------
        * A few examples how to read and make modes for the algorithm
        mode = "newest"
        - Only goes to the previous coordinates when it reaches a dead end (just like the recursive tracking algorithm!!)
        ---------------------------
        mode = "oldest:25,newst:75"
        - When the algorithm reaches a dead end it has 25% chance to go to the oldest coordinates and 75% chance to go the newest coordinates
        ---------------------------
        mode = "newest;oldest;middle,random"
        - When the algoritm reaches the first dead end it will go to the newest
          Next dead end it will go to the oldest
          then the third time it goes to either the middle or the random (50/50 chance)
        This process repeats after 3 dead ends
    '''
        
    def __init__(self, arg):
        ''' Initialize the commands by making a list of modes in a sequence '''
        self.commands = [self.parse_command(cmd) for cmd in arg.split(";")]
        self.current = 0 # The queue position

    def parse_command(self, cmd):
        ''' Function that stores a command in a dictionary with it weight '''
        total_weight = 0
        parts = [] # Each part of the command
        for element in cmd.split(","):
            try:
                name, weight = element.split(":") # seperate the name and weight i.e. "newest:50"
            except:
                name, weight = element, 100 # If there is no weight set it to 100%
            total_weight += int(weight) # have hold of the total weight so we can accurately pick randomly
            parts.append({"name" : name, "weight" : total_weight})
        return {"total_weight": total_weight, "parts": parts} 

    def next_index(self, ceil_index):
        command = self.commands[self.current]
        self.current = (self.current + 1)%len(self.commands)

        random_val = random.randint(0, command["total_weight"] - 1)
        for part in command["parts"]:
            if random_val < part["weight"]:
                if part["name"] == "random":
                    return random.randint(0, ceil_index - 1)
                if part["name"] == "newest":
                    return ceil_index - 1
                if part["name"] == "middle":
                    return ceil_index//2
                if part["name"] == "oldest":
                    return 0

def print_grid(grid, path_grid, pos_index):
    maze_str = ""
    # ╔════════════════════════════╗
    # ║    TOP LINE OF THE MAZE    ║
    # ╚════════════════════════════╝
    maze_str += u'\u2554' # ╔ ; top left corner
    for x in range(width-1):  # width -1 because the right corner will always be "═══╗"
        maze_str += u'\u2550'*3
        # If the path is going south print "╦" else print "═"
        maze_str += u'\u2566' if ((grid[0][x] & E == 0) or (grid[0][x] == 0)) else u'\u2550'
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
            if y*width + x == pos_index:
                path_chr = u'▓'
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
        
def main(grid, path_grid, width, height, mode_str, pos_index):
    cells = []
    mode = Mode(mode_str)
    x,y = random.randint(0, width-1), random.randint(0, height-1)
    path_grid[y][x] = True
    pos_index = y*width + x
    print_grid(grid, path_grid, pos_index)
    time.sleep(1)
    cells.append((x,y))
    while cells != []:
        index = mode.next_index(len(cells))
        x,y = cells[index]
        path_grid[y][x] = True
        directions = [N,S,W,E]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = x + MOVE_X[direction], y + MOVE_Y[direction]
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == 0:
                    grid[y][x] |= direction
                    grid[ny][nx] |= OPPOSITE_DIRECTION[direction]
                    cells.append([nx,ny])
                    index = None
                    path_grid[ny][nx] = True
                    pos_index = ny*width + nx
                    print_grid(grid, path_grid, pos_index)
                    break
                
        
        if index != None:
            px, py = cells[index]
            path_grid[py][px] = False
            del cells[index]
            print_grid(grid, path_grid, pos_index)
    pos_index = None


main(grid, path_grid, width, height, mode_str, pos_index)
print_grid(grid, path_grid, pos_index)