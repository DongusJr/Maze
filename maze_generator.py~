import random
import time, os, sys


FPS = 0.05 # the time it takes to print the grid
CLEAR = lambda: os.system('cls') # function that clears the terminal
width = 21  # Width of the maze
height = 20 # Height of the maze
seed = 2    # Random seed
# random.seed(seed) # Uncomment for a certain seed


# N : 0001
# S : 0010
# W : 0100
# E : 1000
N, S, W, E = 1, 2, 4, 8
# Dictionaries for the maze is carving
MOVE_X_COORDS = {N : 0, S : 0, W : -1, E : 1}
MOVE_Y_COORDS = {N : -1, S : 1, W : 0, E : 0}
OPPOSITE =      {N : S, S : N, W : E, E : W} 


# Grid starts out empty with only 0 and path_grid is the list that holds True if the path is carving on that tile
grid = [[0]*width for i in range(height)]  # Make the grid 10x10 with 0 in every slot
path_grid = [[False]*width for i in range(height)]

def carve_passage_for_maze(current_x, current_y, grid, path_grid):
    ''' The recursive algorithm that carves the grid into a maze

        current_x, current_y : int
            the x and y position of where the algorithm is carving out
        grid : list
            grid that represents which direction each plot goes
        path_grid : list
            boolean grid that represent where the print function can draw the "#" line
    '''
    directions = [N, S, W, E]
    random.shuffle(directions)  # Make the directions random for the maze
    path_grid[current_y][current_x] = True # Mark where the algorithm is running
    display_grid(grid, path_grid)
    for direction in directions:
        # new_x and new_y represent the new x-y coordinates for that certain direction
        new_x, new_y = (current_x + MOVE_X_COORDS[direction]), (current_y + MOVE_Y_COORDS[direction])
        # Make sure the direction is going to a valid spot or not going to one where it has gone before
        if 0 <= new_x <= (len(grid[0]) - 1) and 0 <= new_y <= (len(grid) - 1) and grid[new_y][new_x] == 0:
            grid[current_y][current_x] |= direction  # Add the diretion to the grid for that certain x and y
            grid[new_y][new_x] |= OPPOSITE[direction]  # the new x and y can go the opposite direction
            carve_passage_for_maze(new_x, new_y, grid, path_grid) # Recursive
    path_grid[current_y][current_x] = False  # The recursive function is over here and should be unmarked
    display_grid(grid, path_grid)

def display_grid(grid, path_grid):
    ''' Function that prints out the maze at it current state '''
    # os.system("cls")
    print_grid(grid, path_grid)
    # time.sleep(FPS)


def old_print_grid(grid):
    ''' more simplified way to print out the grid '''
    print(" " + "_"*(width*2 - 1)) # Top of the maze
    for y in range(height):  
        real_line = "|"  # Leftmost part of the maze
        for x in range(width):
            real_line += " " if grid[y][x] & S != 0 else "_" # leave a path south if the path goes south else make a floor under
            if grid[y][x] & E != 0:  # If the path goes east
                real_line += " " if ((grid[y][x] | grid[y][x+1]) & S != 0) else "_" # If it goes east and south there has to be an opening
            else:
                real_line += "|" # If it is not going east there is a wall there
        print(real_line)

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
    # sys.stdout.flush()
    time.sleep(FPS)
    sys.stdout.write(maze_str + "\n")
    

def main(height, grid, path_grid):
    ''' Main function for this program, no particual purpose for now '''
    display_grid(grid, path_grid)
    time.sleep(1)
    carve_passage_for_maze(0, 0, grid, path_grid)
    display_grid(grid, path_grid)


    

main(height, grid, path_grid)
