# More information here
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

# ANSI color codes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# To print colored text to the terminal
# This will work on unixes including OS X, Linux and Windows 
# (provided you use ANSICON, or in Windows 10 provided you enable VT100 emulation).
# There are ANSI codes for setting the color, moving the cursor, and more.
def colprint(text = "", color = bcolors.ENDC):
    print(f"{color}{text}{bcolors.ENDC}")