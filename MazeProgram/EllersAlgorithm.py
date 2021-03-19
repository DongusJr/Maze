from Maze import Maze
from collections import defaultdict
import random
# random.seed(2)

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
        
class EllersAlgorithm(Maze):
    def __init__(self, height = 5, width = 5):
        super().__init__(height, width)
        self.grid = [[0]*width for _ in range(2)]
        self.c_x, self.c_y = -1, -1
        self.top_line_printed = False
        self.number_of_lines = 5

    def fill_maze(self):
        self.display_top_of_maze()
        self.display_line()
        self.display_line(True, True)
        state = State(self.width)
        state.populate()
        row_count = 0

        spinning = True

        while spinning:
            state = self.step(state, row_count)
            state.populate()
            row_count += 1
            spinning = row_count + 1 < self.height
        
        state = self.step(state, row_count, True)
        

        # for i in range(self.width):
        #     if self.get_cell(0, i) & S != 0:
        #         self.add_direction_to_grid(1, i, N)

        # self.display_line(True)

    def add_east_and_west_to_set(self, connected_set, set_index_modifier, row_count):
        for index in range(len(connected_set)):
            y = 0 if row_count == 0 else 1
            modified_index = index + set_index_modifier
            last = (index + 1 == len(connected_set))
            direction = 0 if last else E
            self.add_direction_to_grid(y, modified_index, direction)      
            direction = W if 0 < index else 0
            self.add_direction_to_grid(y, modified_index, direction)      

    def add_mark_on_cells(self, connected_set, set_index_modifier, mark_bool, row_count):
        for index in range(len(connected_set)):
            y = 0 if row_count == 0 else 1
            modified_index = index + set_index_modifier
            self.mark_grid(y, modified_index, mark_bool)

    def display_grid_with_new_direction_and_path(self, connected_set, set_index_modifier, row_count):
        self.add_mark_on_cells(connected_set, set_index_modifier, True, row_count)
        self.add_east_and_west_to_set(connected_set, set_index_modifier, row_count)
        self.reset_line(self.number_of_lines)
        if row_count == 0 or row_count == 1:
            self.display_top_of_maze()
        self.display_line()
        self.display_line(True, True)
        self.add_mark_on_cells(connected_set, set_index_modifier, False, row_count)


    def step(self, state, row_count, finish=False):
        connected_sets = []
        connected_set = [0]

        set_index_modifier = 0
        for c in range(state.get_width() - 1):
            if state.same_cell(c, c+1) or (not finish and random.randint(0,1) > 0):
                connected_sets.append(connected_set)
                self.display_grid_with_new_direction_and_path(connected_set, set_index_modifier, row_count)
                #print grid
                set_index_modifier += len(connected_set)
                connected_set = [c+1]
            else:
                state.merge(c, c+1)
                connected_set.append(c+1)
                self.display_grid_with_new_direction_and_path(connected_set, set_index_modifier, row_count)
                # display grid
        
        connected_sets.append(connected_set)

        
        if row_count == 1:
            self.number_of_lines = 4
            self.reset_line(self.number_of_lines)
            self.top_line_printed = True
            self.display_line()
            self.grid.pop(0)
            self.grid.append([0]*self.width)
            self.display_line()
            self.display_line(True, True)
        elif row_count != 0:
            self.reset_line(self.number_of_lines)
            self.display_line()
            self.grid.pop(0)
            if not finish:
                self.grid.append([0]*self.width)
                self.display_line()
                self.display_line(True, True)
            else:
                self.grid.insert(0,[0]*self.width)
                self.display_line(True, True)

        verticals = []
        next_state = state.next()
        if not finish:
            for id_, set_ in sorted(state.get_sets().items()):
                random.shuffle(set_)
                random_factor = 1 if len(set_) == 1 else len(set_) - 1
                cells_to_connect = set_[0 : 1 + random.randint(0, random_factor)]
                verticals += cells_to_connect
                for cell in cells_to_connect:
                    next_state.add(cell, id_)
                    self.add_and_display_vertical(cell, row_count)
                    # Display grid


        return next_state
                    
            
    def add_and_display_vertical(self, cell, row_count):
        self.add_direction_to_grid(0, cell, S)
        self.add_direction_to_grid(1, cell, N)
        self.mark_grid(0, cell, True)
        self.mark_grid(1, cell, True)
        self.reset_line(self.number_of_lines)
        if row_count == 0:
            self.display_top_of_maze()
        self.display_line()
        self.display_line(True, True)
        self.mark_grid(0, cell, False)
        self.mark_grid(1, cell, False)

if __name__ == "__main__":
    maze = EllersAlgorithm(20, 20)
    maze.fill_maze()
    # maze.display_maze()
    # maze.display_line(0)
    # print(maze.grid)
        