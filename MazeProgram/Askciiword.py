''' letters_askii.txt is exential for this class '''
''' ascii box:
    ╔═╗
    ╚═╝
'''


class AskiiWord:
    ''' Function that creates a ascii version of a text 

        class variables
        ---------------
        alphabetic_mask : dictionary that holds double encapulated list
            in letters_askii.txt is a "picture" of each letter in the alphabet where "X" represent
            where a box is for the the ascii art, "O" is an empty space. a boolean value is used
            to represent where boxes are and where they are not
    '''
    def __init__(self, word):
        self.alphabetic_mask = self.make_alpha_mask()
        self.askii_word_lis = self.make_askii_text(word)
        self.height_of_word = 5
        self.length_of_word = len(self.askii_word_lis[0])

    def get_askii_word(self):
        ''' Function that returns a list of chr for the ascii text '''
        return self.askii_word_lis

    def get_height(self):
        ''' Function that returns the height of the word (y size) '''
        return self.height_of_word

    def get_length(self):
        ''' Function that returns the width of the word (x size) '''
        return self.length_of_word

    def add_line_to_lis(self, line, chr_number, alphabetic_mask):
        ''' Function that adds a line from a txt to the alphabetic mask, using boolean
            to represent whether a box is present or not
        '''
        temp_lis = []
        for char in line:
            if char == "X": # Box present
                temp_lis.append(True)
            elif char == "O": # Box not present
                temp_lis.append(False)
        alphabetic_mask[chr(chr_number)].append(temp_lis) # Add the list to the mask

    def make_empty_mask(self):
        ''' Function that makes an empty alphabetic mask dict of each letter in the alphabet '''
        alphabetic_mask = {}
        for i in range(97, 123): # from a - z
            alphabetic_mask[chr(i)] = []
        alphabetic_mask[" "] = [] # Also space
        return alphabetic_mask

    def make_alpha_mask(self):
        ''' Function that creates a true/false list for each letter in the alphabet representing their ascii mask '''
        alphabetic_mask = self.make_empty_mask()
        with open("Text_files/letters_askii.txt", "r") as f:
            chr_number = 97 # a
            for line in f:
                line = line.strip()
                if line == "": # Empty line represent a new chr is next
                    if chr_number != 122:
                        chr_number += 1 # Go to next letter
                    else:
                        # done a-z, now have to make a mask for space(" ")
                        chr_number = 32
                else:
                    self.add_line_to_lis(line, chr_number, alphabetic_mask)
        return alphabetic_mask

    def make_word_mask(self, text):
        ''' Function that makes a mask for a text '''
        text_lis = []
        for i in range(5):
            temp_lis = []
            for letter in text:
                temp_lis += self.alphabetic_mask[letter][i]
                temp_lis += [False]
            text_lis.append(temp_lis)
        return text_lis

    def make_top_line(self):
        ''' Function that creates the top line of the ascii text '''
        ascii_str = ""
        for x in range(len(self.text_lis[0])):
            if not self.contains(0, x):
                if x != len(self.text_lis[0]) - 1:
                    if x != 0:
                        ascii_str += "  " if not self.contains(0, x+1) else " "
                    else:
                        ascii_str += "  "
            else:
                try:
                    if not self.contains(0, x-1):
                        ascii_str += u'╔═'
                    else:
                        ascii_str += u'╦═'
                except:
                    ascii_str += u'╔═'
                try:
                    if not self.contains(0, x+1):
                        ascii_str += u'╗' 
                except:
                    ascii_str += u'╗'
        return ascii_str

    def make_askii_text(self, text):
        ''' Function that creates the ascii text '''

        ''' I made this program some time ago for another project, I'm not going to comment this function because
            it is exteremely confusing, even with comments. I had to do alot of trail and error to 
            get it to work but each comment would be something like:
            "If there is a box at this coordinates but not in x+1 and y+1, than this happens"
        '''
        self.text_lis = self.make_word_mask(text.lower())
        ascii_str_lis = [self.make_top_line()]
        ascii_str = ""
        for y in range(5):
            try:
                if (not self.contains(y+1, 0)) and (not self.contains(y, 0)):
                    ascii_str += " "
                elif self.contains(y, 0) and self.contains(y+1, 0):
                    ascii_str += u'╠'
                elif (not self.contains(y, 0) and self.contains(y+1, 0)):
                    ascii_str += u'╔'
                else:
                    ascii_str += u'╚'
            except:
                if not self.contains(y, 0):
                    ascii_str += " "
                else:
                    ascii_str += u'╚'

            for x in range(0, len(self.text_lis[0])):
                try:
                    if self.contains(y,x):
                        ascii_str += u'═'
                    elif not self.contains(y, x) and not self.contains(y+1, x):
                        ascii_str += " "
                    else:
                        ascii_str += u'═'
                except:
                    # y == 4
                    ascii_str += u'═' if self.contains(y, x) else " "
                try:
                    if self.contains(y, x) and self.contains(y+1, x+1) or (self.contains(y+1, x) and self.contains(y, x+1)):
                        ascii_str += u'╬'
                    elif self.contains(y,x) and (self.contains(y, x+1) or self.contains(y+1, x+1)):
                        ascii_str += u'╩'
                    elif self.contains(y, x) and self.contains(y+1, x):
                        ascii_str += u'╣'
                    elif self.contains(y, x):
                        ascii_str += u'╝'
                    elif not self.contains(y, x) and self.contains(y+1, x) and self.contains(y, x+1):
                        ascii_str += u'╬'
                    elif not self.contains(y, x) and self.contains(y+1, x) and self.contains(y+1, x+1):
                        ascii_str += u'╦'
                    elif not self.contains(y, x) and self.contains(y, x+1) and self.contains(y+1, x+1):
                        ascii_str += u'╠'
                    elif not self.contains(y, x) and self.contains(y+1, x):
                        ascii_str += u'╗'
                    elif not self.contains(y, x) and self.contains(y, x+1):
                        ascii_str += u'╚'
                    elif not self.contains(y, x) and self.contains(y+1, x+1):
                        ascii_str += u'╔'
                    else:
                        ascii_str += " "
                except:
                    if y == 4 and x == len(self.text_lis[0]) - 1:
                        ascii_str += u'╝' if self.contains(y, x) else " "
                    elif y == 4:
                        if self.contains(y, x) and self.contains(y, x+1):
                            ascii_str += u'╩'
                        elif self.contains(y, x):
                            ascii_str += u'╝'
                        elif not self.contains(y, x) and self.contains(y, x+1):
                            ascii_str += u'╚'
                        else:
                            ascii_str += " "
                    elif x == len(self.text_lis[0]) - 1:
                        if self.contains(y, x) and self.contains(y+1, x):
                            ascii_str += u'╣'
                        elif self.contains(y, x):
                            ascii_str += u'╝'
                        elif not self.contains(y, x) and self.contains(y+1, x):
                            ascii_str += u'╗'
                        else:
                            ascii_str += " "
            ascii_str_lis.append(ascii_str)
            ascii_str = ""
        return ascii_str_lis

    def contains(self, y, x):
        return self.text_lis[y][x] == True



if __name__ == "__main__":
    askii_w = AskiiWord("Hangman")
    for y in range(len(askii_w.askii_word)):    
        print(askii_w.askii_word[y])
        
            
