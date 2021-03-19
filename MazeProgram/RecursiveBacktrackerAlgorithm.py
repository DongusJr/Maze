from Maze import Maze
import random
# random.seed(5)

N, S, W, E = 1, 2, 4, 8

class RecursiveBacktrackerAlgorithm(Maze):
    def __init__(self,height = 5, width = 5, do_display_maze = True):
        super().__init__(height, width)
        self.c_x = random.randint(0, self.width - 1)
        self.c_y = random.randint(0, self.height - 1)
        self.do_display_maze = do_display_maze

    def fill_maze(self):
        self.carve_passage_for_maze(self.c_y, self.c_x)
        self.set_x_and_y(-1, -1)
        if self.do_display_maze:
            self.display_maze()

    def carve_passage_for_maze(self, c_y, c_x, diplay_maze = True):
        directions = [N, S, W, E]
        random.shuffle(directions)
        self.mark_grid(c_y, c_x, True)
        if self.do_display_maze:
            self.display_maze()
        for direction in directions:
            new_x, new_y = self.get_new_coords_after_move(c_y, c_x, direction)
            if self.is_in_grid(new_y, new_x) and not self.grid_is_marked(new_y, new_x):
                self.add_direction_to_grid(c_y, c_x, direction)
                self.add_direction_to_grid(new_y, new_x, self.opposite[direction])
                self.set_x_and_y(new_y, new_x)
                self.carve_passage_for_maze(new_y, new_x) # Recurse   
                self.set_x_and_y(c_y, c_x)
                if self.do_display_maze:
                    self.display_maze()
        self.mark_grid(c_y, c_x, False)
        

if __name__ == "__main__":
    maze = RecursiveBacktrackerAlgorithm(25, 50)
    # print(maze)            
    maze.fill_maze()
    # print(maze)

        

    
