import random
from collections import defaultdict
import sys, time

from ctypes import *

FPS = 0
width = 50
height = 25
seed = 10
# random.seed(9) 

N, S, W, E = 1, 2, 4, 8

class State:
    def __init__(self, width, next_set = -1):
       self.width = width
       self.next_set = next_set
       self.sets = defaultdict(list)
       self.cells = {}

    def get_sets(self):
        return self.sets

    def get_width(self):
        return self.width

    def next(self):
        return State(self.width, self.next_set)

    def populate(self):
        for cell in range(self.width):
            try:
                self.cells[cell]
                continue
            except:
                self.next_set += 1
                self.sets[self.next_set].append(cell)
                self.cells[cell] = self.next_set

    def merge(self, sink_cell, target_cell):
        sink, target = self.cells[sink_cell], self.cells[target_cell]

        self.sets[sink] += self.sets[target]
        for cell in self.sets[target]:
            self.cells[cell] = sink
        del self.sets[target]

    def same_cell(self, cell_1, cell_2):
        return self.cells[cell_1] == self.cells[cell_2]

    def add(self, cell, set_):
        self.cells[cell] = set_
        self.sets[set_].append(cell)

def print_grid(grid, path_grid):
    maze_str = ""
    # ╔════════════════════════════╗
    # ║    TOP LINE OF THE MAZE    ║
    # ╚════════════════════════════╝
    maze_str += u'\u2554' # ╔ ; top left corner
    for x in range(len(grid[0])-1):  # width -1 because the right corner will always be "═══╗"
        maze_str += u'\u2550'*3
        # If the path is going south print "╦" else print "═"
        maze_str += u'\u2566' if ((grid[0][x] & E == 0) or (grid[0][x] == 0)) else u'\u2550'
    maze_str += u'\u2550'*3 + u'\u2557' + "\n" # "═══╗"
    # ╔════════════════════════════╗
    # ║     REST OF THE MAZE       ║
    # ╚════════════════════════════╝
    for y in range(len(grid)):
        # ╔════════════════════════════╗
        # ║    LEFT LINE OF THE MAZE   ║
        # ╚════════════════════════════╝
        # first_line is the middle line of the box where grid[y][x] is  [2x4]
        # second line is the lower line of the box where grid[y][x] is
        first_line = u'\u2551' # "║", it is always this
        if y == len(grid) - 1:
            second_line = u'\u255a' # "╚" for the left down corner
        else:
            second_line = u'\u2560' if (grid[y][0] & E != 0 and grid[y][0] & S == 0) else u'\u2551' # "╠" if the block is going east and not south else "║"
        # ╔════════════════════════════╗
        # ║      REST OF THE MAZE      ║
        # ║     2  LINES EACH LOOP     ║
        # ╚════════════════════════════╝   
        for x in range(len(grid[0])):
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
            
            try:
                if grid[y+1][x] == 0:
                    second_line_begin = u'\u2550'*3
                else:
                    raise
            except:
                second_line_begin = " " + path_chr + " "

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
                    if y == len(grid) - 1 and x == len(grid[0]) - 1:  # If it is the down left corner
                        second_line += u'\u2550'*3 + u'\u255d' # "═══╝"
                    elif y == len(grid) -1:  # If it is on the bottom line
                        second_line += u'\u2550'*3 + u'\u2569' # "═══╩"
                    else:  # If everything else fails, should be this one I hope xd
                        second_line += u'\u2550'*3 + u'\u2563' # "═══╣"
            # For grid numbers 2, 3, 6 and 7(S, N^S, S^W, S^W^N)
            elif grid[y][x] & E == 0:
                try:
                    if (grid[y][x+1] & S == 0 and grid[y+1][x] & E == 0):
                        second_line += second_line_begin + u'\u2560' # "   ╠"
                    elif (grid[y][x+1] & S == 0):
                        second_line += second_line_begin + u'\u255a' # "   ╚"
                    else:
                        raise
                except:
                    second_line += second_line_begin + u'\u2551' # "   ║"
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
                        second_line += second_line_begin + u'\u2554' # "   ╔"
                    elif grid[y+1][x] & E == 0 and grid[y][x+1] & S != 0:
                        second_line += second_line_begin + u'\u2551' # "   ║"
                    else:
                        raise
                except:
                    second_line += second_line_begin + u'\u2550' # "   ═"
        maze_str += first_line + "\n"
        maze_str += second_line + "\n"
    # CLEAR() # Clear the terminal
    # print()
    sys.stdout.write("\r" + "\n"*(51-(len(grid)*2 + 1)) + "{}".format("\n" + maze_str))
    # sys.stdout.flush()
    time.sleep(FPS)

def row_to_str(row, last = False):
    s = "|"
    for index, cell in enumerate(row):
        south = (cell & S != 0)
        try:
            next_south = (row[index+1] and row[index+1] & S != 0)
        except:
            next_south = False
        east = (cell & E != 0)

        s += " " if south else "_"

        if east:
            s += " " if (south or next_south) else "_"
        else:
            s += "|"

    return s

def step(state, grid, path_grid, row_count, finish = False):
    connected_sets = []
    connected_set = [0]

    set_index_modifier = 0
    for c in range(state.get_width() - 1):
        if state.same_cell(c, c+1) or (not finish and random.randint(0,1) > 0):
            connected_sets.append(connected_set)
            display_grid(connected_set, row_count, set_index_modifier, grid, path_grid, True)
            set_index_modifier += len(connected_set)
            connected_set = [c+1]
        else:
            state.merge(c, c+1)
            connected_set.append(c+1)
            display_grid(connected_set, row_count, set_index_modifier, grid, path_grid, True)
    
    print_grid(grid, path_grid)
    connected_sets.append(connected_set)

    verticals = []
    next_state = state.next()

    if not finish:
        grid.append([0]*len(grid[0]))
        for id_, set_ in sorted(state.get_sets().items()):
            random.shuffle(set_)
            random_factor = 1 if len(set_) == 1 else len(set_) - 1
            cells_to_connect = set_[0 : 1 + random.randrange(0, random_factor)]
            verticals += cells_to_connect
            for cell in cells_to_connect:
                next_state.add(cell, id_)
                grid[row_count][cell] |= S
                grid[row_count + 1][cell] |= N
                path_grid[row_count][cell], path_grid[row_count+1][cell] = True, True
                print_grid(grid, path_grid)
                path_grid[row_count][cell], path_grid[row_count+1][cell] = False, False
                # time.sleep(FPS)

    return next_state

def display_grid(connected_set, row_count, set_index_modifier, grid, path_grid, bool_val):
    mark_in_grid(connected_set, row_count, set_index_modifier, grid)
    mark_path(connected_set, row_count, set_index_modifier, path_grid, bool_val)
    print_grid(grid, path_grid)
    mark_path(connected_set, row_count, set_index_modifier, path_grid, not bool_val)
    # time.sleep(FPS)
    

def mark_path(connected_set, row_count, set_index_modifier, path_grid, bool_val):
    for index in range(len(connected_set)):
        modified_index = index + set_index_modifier
        path_grid[row_count][modified_index] = bool_val

def mark_in_grid(connected_set, row_count, set_index_modifier, grid):
    for index in range(len(connected_set)):
        modified_index = index + set_index_modifier
        last = (index + 1 == len(connected_set))
        grid[row_count][modified_index] |= 0 if last else E
        grid[row_count][modified_index] |= W if 0 < index else 0
        



def main(width):
    state = State(width)
    state.populate()
    row_count = 0

    spinning = True

    maze_grid = [[0]*width]
    path_grid = [[False]*width for i in range(height)]

    while spinning:
        print_grid(maze_grid, path_grid)
        state = step(state, maze_grid, path_grid, row_count)
        state.populate()
        row_count += 1
        spinning = row_count+1 < height

    state = step(state, maze_grid, path_grid, row_count, True)
    row_count += 1

    for i in range(width):
        if maze_grid[row_count-2][i] & S != 0:
            maze_grid[row_count-1][i] |= N

    print_grid(maze_grid, path_grid)

main(width)
    
