
def add_line_to_lis(line, chr_number, alphabetic_mask):
    temp_lis = []
    for char in line:
        if char == "X":
            temp_lis.append(True)
        elif char == "O":
            temp_lis.append(False)
    alphabetic_mask[chr(chr_number)].append(temp_lis)

    # temp_lis = []
    # for i in range(5):
    #     for i in range(3):
    #         temp_lis.append(False)
    #     alphabetic_mask[" "].append(temp_lis)

def make_empty_mask():
    alphabetic_mask = {}
    for i in range(97, 123):
        alphabetic_mask[chr(i)] = []
    alphabetic_mask[" "] = []
    return alphabetic_mask

def make_alpha_mask():
    alphabetic_mask = make_empty_mask()
    with open("letters_askii.txt", "r") as f:
        chr_number = 97 # a
        for line in f:
            line = line.strip()
            if line == "":
                if chr_number != 122:
                    chr_number += 1
                else:
                    chr_number = 32
            else:
                add_line_to_lis(line, chr_number, alphabetic_mask)
    return alphabetic_mask

def make_word_mask(alphabetic_mask, text):
    text_lis = []
    for i in range(5):
        temp_lis = []
        for letter in text:
            temp_lis += alphabetic_mask[letter][i]
            temp_lis += [False]
        text_lis.append(temp_lis)
    return text_lis

def make_top_line(text_lis):
    ascii_str = ""
    for x in range(len(text_lis[0])):
        if text_lis[0][x] == False:
            if x != len(text_lis[0]) - 1:
                if x != 0:
                    ascii_str += "  " if text_lis[0][x+1] == False else " "
                else:
                    ascii_str += "  "
        else:
            try:
                if text_lis[0][x-1] == False:
                    ascii_str += u'╔═'
                else:
                    ascii_str += u'╦═'
            except:
                ascii_str += u'╔═'
            try:
                if text_lis[0][x+1] == False:
                    ascii_str += u'╗' 
            except:
                ascii_str += u'╗'
    ascii_str += "\n"
    return ascii_str

def make_askii_text(alphabetic_mask, text):
    text_lis = make_word_mask(alphabetic_mask, text.lower())

    ascii_str = make_top_line(text_lis)
    
    for y in range(5):
        try:
            if text_lis[y+1][0] == False and text_lis[y][0] == False:
                ascii_str += " "
            elif text_lis[y][0] == True and text_lis[y+1][0] == True:
                ascii_str += u'╠'
            elif text_lis[y][0] == False and text_lis[y+1][0] == True:
                ascii_str += u'╔'
            else:
                ascii_str += u'╚'
        except:
            if text_lis[y][0] == False:
                ascii_str += " "
            else:
                ascii_str += u'╚'

        for x in range(0, len(text_lis[0])):
            try:
                if text_lis[y][x] == True:
                    ascii_str += u'═'
                elif text_lis[y][x] == False and text_lis[y+1][x] == False:
                    ascii_str += " "
                else:
                    ascii_str += u'═'
            except:
                # y == 4
                ascii_str += u'═' if text_lis[y][x] == True else " "
            try:
                if text_lis[y][x] == True and (text_lis[y+1][x+1] == True or (text_lis[y+1][x] == True and text_lis[y][x+1] == True)):
                    ascii_str += u'╬'
                elif text_lis[y][x] == True and (text_lis[y][x+1] == True or text_lis[y+1][x+1] == True):
                    ascii_str += u'╩'
                elif text_lis[y][x] == True and text_lis[y+1][x] == True:
                    ascii_str += u'╣'
                elif text_lis[y][x] == True:
                    ascii_str += u'╝'
                elif text_lis[y][x] == False and text_lis[y+1][x] == True and (text_lis[y][x+1] == True):
                    ascii_str += u'╬'
                elif text_lis[y][x] == False and text_lis[y+1][x] == True and text_lis[y+1][x+1] == True:
                    ascii_str += u'╦'
                elif text_lis[y][x] == False and text_lis[y][x+1] == True and text_lis[y+1][x+1] == True:
                    ascii_str += u'╠'
                elif text_lis[y][x] == False and text_lis[y+1][x] == True:
                    ascii_str += u'╗'
                elif text_lis[y][x] == False and text_lis[y][x+1] == True:
                    ascii_str += u'╚'
                elif text_lis[y][x] == False and text_lis[y+1][x+1] == True:
                    ascii_str += u'╔'
                else:
                    ascii_str += " "
            except:
                if y == 4 and x == len(text_lis[0]) - 1:
                    ascii_str += u'╝' if text_lis[y][x] else " "
                elif y == 4:
                    if text_lis[y][x] == True and text_lis[y][x+1] == True:
                        ascii_str += u'╩'
                    elif text_lis[y][x] == True:
                        ascii_str += u'╝'
                    elif text_lis[y][x] == False and text_lis[y][x+1] == True:
                        ascii_str += u'╚'
                    else:
                        ascii_str += " "
                elif x == len(text_lis[0]) - 1:
                    if text_lis[y][x] == True and text_lis[y+1][x] == True:
                        ascii_str += u'╣'
                    elif text_lis[y][x] == True:
                        ascii_str += u'╝'
                    elif text_lis[y][x] == False and text_lis[y+1][x] == True:
                        ascii_str += u'╗'
                    else:
                        ascii_str += " "

        print(ascii_str)
        ascii_str = ""
        # ascii_str += "\n"

    # print(ascii_str)



def main():
    ascii_text = input("What to do you want ascii-fied: ")
    alphabetic_mask = make_alpha_mask()
    make_askii_text(alphabetic_mask, ascii_text)



main()
        
            
