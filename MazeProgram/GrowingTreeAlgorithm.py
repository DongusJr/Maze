from Maze import Maze
import random

N, S, W, E = 1, 2, 4, 8


class Mode:
    def __init__(self, arg):
        self.commands = [self.parse_commands(cmd) for cmd in arg.split(";")]
        self.current = 0

    def parse_commands(self, cmd):
        total_weight = 0
        parts = []
        for element in cmd.split(","):
            try:
                name, weight = element.split(":")
            except:
                name, weight = element, 100
            total_weight += int(weight)
            parts.append({"name" : name, "weight" : total_weight})
        return {"total_weight" : total_weight, "parts" : parts}

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

class GrowingTreeAlgorithm(Maze):
    def __init__(self, height = 5, width = 5, mode_str = "random"):
        super().__init__(height, width)
        self.mode = Mode(mode_str)

    def fill_maze(self):
        cells = []
        self.c_x, self.c_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.mark_grid(self.c_y, self.c_x, True)
        self.display_maze()
        cells.append((self.c_x,self.c_y))
        while cells != []:
            index = self.mode.next_index(len(cells))
            self.c_x, self.c_y = cells[index]
            self.mark_grid(self.c_y, self.c_x, True)
            directions = [N, S, W, E]
            random.shuffle(directions)
            for direction in directions:
                nx, ny = (self.c_x + self.move_x[direction]), (self.c_y + self.move_y[direction])
                if self.is_in_grid(ny,nx) and not self.grid_is_marked(ny, nx):
                    self.add_direction_to_grid(self.c_y, self.c_x, direction)
                    self.add_direction_to_grid(ny, nx, self.opposite[direction])
                    cells.append([nx, ny])
                    self.mark_grid(ny, nx, True)
                    index = None
                    self.display_maze()
                    break

            if index != None:
                px, py = cells[index]
                self.mark_grid(py, px, False)
                del cells[index]
                self.display_maze()
        
        self.c_x, self.c_y = -1, -1
        self.display_maze()

if __name__ == "__main__":
    maze = GrowingTreeAlgorithm(1, 1, "random:75,newest:25")
    maze.fill_maze()

