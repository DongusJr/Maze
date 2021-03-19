from ctypes import windll, create_string_buffer

class Interface:
    def __init__(self):
        self.set_window_size()

    def set_window_size(self):
        ''' Function that with some voodoo magic can determine the size of a window of a terminal '''
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

        if res:
            import struct
            (bufx, bufy, curx, cury, wattr,
            left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            self.w_size_x = right - left + 1
            self.w_size_y = bottom - top + 1
        else:
            sizex, sizey = 80, 25 # can't determine actual size - return default values
                    
    def get_block_size(self):
        ''' Returns the block size of the terminal,
            block size is the amount of blocks in a maze can fit on the screen '''
        return self.w_size_x//4, self.w_size_y//2

    def __str__(self):
        return "x : " + str(self.w_size_x) + ", y : " + str(self.w_size_y)

if __name__ == "__main__":
    interface = Interface()
    print(interface)