from RecursiveBacktrackerAlgorithm import RecursiveBacktrackerAlgorithm
from ctypes import windll, create_string_buffer
import sys
from Askciiword import AskiiWord

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

class FakeWindow:
    def __init__(self, maze_backround = False):
        self.w_x_size, self.w_y_size = self._get_window_size()
        self.window = [[""]*self.w_x_size for _ in range(self.w_y_size)]
        if maze_backround:
            self.make_maze_background()

    def make_maze_background(self):
        self.m_x_size, self.m_y_size = self.w_x_size//4, self.w_y_size//2 - 1
        maze = RecursiveBacktrackerAlgorithm(self.m_y_size, self.m_x_size, do_display_maze=False)
        maze.fill_maze()
        maze_str = maze.get_maze_str().split("\n")
        for y in range(self.w_y_size):
            for x in range(self.w_x_size):
                try:
                    self.window[y][x] = maze_str[y][x]
                except:
                    pass

    def _get_window_size(self):
        ''' Some voodoo magic code I found on the net some time ago which gives amount of spaces and newlines
            a terminal/cmd can hold, representing the x and y axiss of the window '''
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

        if res:
            import struct
            (buf_x, buf_y, cur_x, cur_y, wattr,
            left, top, right, bottom, max_x, max_y) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            size_x = right - left + 1
            size_y = bottom - top + 1
        else:
            sizex, sizey = 80, 25 
            # can't determine actual size - return default values
        return (size_x, size_y)

    def display_window(self):
        for y in range(self.w_y_size):
            for x in range(self.w_x_size):
                sys.stdout.write(self.window[y][x])
            sys.stdout.write("\n")

    def make_box(self, box_x_size, box_y_size):
        box_x_pos = ((self.w_x_size - box_x_size) // 2)
        box_y_pos = ((self.w_y_size - box_y_size) // 2)
        box_x_end = box_x_pos + box_x_size
        box_y_end = box_y_pos + box_y_size
        for y in range(box_y_pos, box_y_end + 1):
            for x in range(box_x_pos, box_x_end + 1):
                window_chr = ""
                if y == box_y_pos and x == box_x_pos:
                    window_chr = TOP_LEFT_CORNER
                elif y == box_y_pos and x == box_x_end:
                    window_chr = TOP_RIGHT_CORNER
                elif y == box_y_end and x == box_x_pos:
                    window_chr = BOT_LEFT_CORNER
                elif y == box_y_end and x == box_x_end:
                    window_chr = BOT_RIGHT_CORNER
                elif x == box_x_pos or x == box_x_end:
                    window_chr = VERT_WALL
                elif y ==  box_y_pos or y == box_y_end:
                    window_chr = HORZ_WALL
                else:
                    window_chr = " "
                self.window[y][x] = window_chr
                
    def make_header(self, offset, word):
        ascii_word = AskiiWord(word)
        

if __name__ == "__main__":
    test = FakeWindow(True)
    test.make_box(100, 42)
    test.display_window()
