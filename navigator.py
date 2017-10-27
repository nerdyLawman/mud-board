#!/usr/bin/env python

import time
from blessed import Terminal

def main():

    term = Terminal()
    screen = ""

    print(term.clear())
    screen += term.move(0,0) + "up top, bro"
    screen += term.move(term.height - 3, 0) + "http://horriblevacuum.com"
    cmd = ""
    while cmd != "exit":
        print(term.move(0, 0) + term.clear_eos() + screen)
        cmd = raw_input("Enter: ")

    third = term.width/3
    tthird = (term.width/3)*2

    print(term.clear())
    print(term.on_blue(" ") * term.width)
    print(term.move(0,0))
    print(term.cyan_on_blue("tel:") + term.move_x(third) + term.bright_magenta_on_blue("666-666-6666") + term.move_x(tthird) + "HET")
    print(term.cyan_on_blue("tel:") + term.move_x(third) + "666-666-6666")
    print(term.cyan_on_blue("tel:") + term.move_x(third) + "666-666-6666")
    print(term.on_black(" ") * term.width)
    print(term.on_bright_red(" ") * term.width)
    print(term.on_bright_green(" ") * term.width)
    print(term.on_bright_yellow(" ") * term.width)
    print(term.on_bright_blue(" ") * term.width)
    print(term.on_bright_magenta(" ") * term.width)
    print(term.on_bright_cyan(" ") * term.width)
    print(term.on_bright_white(" ") * term.width)

if __name__ == '__main__':
    main()
