import time, os, sys
from Getch import _Getch

class ListIsEmptyException(Exception):
    pass

class LinkedList:
    class _LinkedNode:
        def __init__(self, data, next):
            self.data = data
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def push_front(self, data):
        if self.head == None:
            self.head = self._LinkedNode(data, None)
        else:
            new_node = self._LinkedNode(data, self.head)
            self.head = new_node
        self.size += 1
            
    def pop_front(self):
        if self.size == 0:
            raise ListIsEmptyException()
        new_head = self.head.next
        self.head.next = None
        return_value = self.head.data
        self.head = new_head
        self.size -= 1
        return return_value

    def __len__(self):
        return self.size

class Stack:
    def __init__(self):
        self._stack = LinkedList()

    def __len__(self):
        return len(self._stack)

    def add(self, data):
        self._stack.push_front(data)

    def remove(self):
        return self._stack.pop_front()


FPS = 0
width = 5
height = 5

N, S, W, E = 1, 2, 4, 8
MOVE_X_COORDS = {N : 0, S : 0, W : -1, E : 1}
MOVE_Y_COORDS = {N : -1, S : 1, W : 0, E : 0}
OPPOSITE =      {N : S, S : N, W : E, E : W}

grid = [[0]*width for _ in range(height)]
path_grid = [[False]*width for i in range(height)]

def make_maze(current_x, current_y, grid, path_grid):
    previous_moves = Stack()
    grid_count = 1
    while grid_count <= len(grid[0]) * len(grid) - 1:
        path_grid[current_y][current_x] = True
        print_grid(grid, path_grid)
        direction, go_back = get_input_from_user(previous_moves)
        try:
            new_x, new_y = (current_x + MOVE_X_COORDS[direction]), (current_y + MOVE_Y_COORDS[direction])
        except:
            path_grid[current_y][current_x] = False
            direction, x_and_y = direction
            current_x, current_y = x_and_y
            new_x, new_y = (current_x + MOVE_X_COORDS[OPPOSITE[direction]]), (current_y + MOVE_Y_COORDS[OPPOSITE[direction]])
        if 0 <= new_x <= (len(grid[0]) - 1) and 0 <= new_y <= (len(grid) - 1):
            if go_back == False and grid[new_y][new_x] == 0:
                previous_moves.add((direction, (new_x, new_y)))
            if grid[new_y][new_x] == 0 and go_back == False:
                grid_count += 1
                grid[current_y][current_x] |= direction
                grid[new_y][new_x] |= OPPOSITE[direction]
            elif go_back == True:
                grid_count -= 1
                grid[current_y][current_x] = grid[current_y][current_x] ^ OPPOSITE[direction]
                grid[new_y][new_x] = grid[new_y][new_x] ^ direction
            path_grid[current_y][current_x] = False
            current_x = new_x
            current_y = new_y 

        print(grid_count)      
    print_grid(grid, path_grid)


def get_input_from_user(previous_moves):
    arrow_pressed = False
    key_input = _Getch()
    while True:
        k = key_input()
        if arrow_pressed:
            if k == b'M': # Right
                return E, False
            elif k == b'K': # Left
                return W, False
            elif k == b'H': # Up
                return N, False
            else:           # Down
                return S, False
        if k == b'\x03': # ctrl + c
            quit()
        if k == b'\xe0' or k == b'\x00': # Arrow
            arrow_pressed = True
        if k == b'\x08': # Backspace
            try:
                previous_move = previous_moves.remove()
                return previous_move, True
            except ListIsEmptyException:
                pass


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


if __name__ == "__main__":
    make_maze(0,0, grid, path_grid)