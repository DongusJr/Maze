import os, sys, time

from colorama import init, Fore, Back, Style
init()

str_test = Fore.BLACK + Back.WHITE + "Test" + Style.RESET_ALL
print(str_test)
print('back to normal now')
sys.stdout.write("hello world" + "\n")
time.sleep(1)
sys.stdout.write("\u001b[1A")
sys.stdout.write("\u001b[11D")
sys.stdout.write("\u001b[0K")
sys.stdout.write("\u001b[11D")
# sys.stdout.write("hello world")
