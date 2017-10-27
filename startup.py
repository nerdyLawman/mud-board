#!/usr/bin/env python

from blessed import Terminal
import time

def main():

    screen = ""
    line = 0
    col = 0
    out = ""

    term = Terminal()
    print(term.clear())
    for i in range(50):
        out = term.bright_cyan("loop: ") + term.bright_yellow(str(i))
        print(term.move(line,col) + screen + out)
        time.sleep(0.02)
    screen += out + "\n\r"
    for i in range(2500,3500,10):
        out = term.bright_cyan("buffering: ") + term.bright_yellow(str(i))
        print(term.move(line,col) + screen + out)
        time.sleep(0.02)
    screen += out + "\n\r"
    for i in range(2,39):
        out = term.on_bright_blue(" ") * i
        print(term.move(line,col) + screen + out)
        time.sleep(0.05)
    screen += out
    outlines = ["Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "I've never been much for ceremony",
        "Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "I've never been much for ceremony",
        "Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "I've never been much for ceremony",
        "Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "I've never been much for ceremony",
        "Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "I've never been much for ceremony",
        "Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",
        "I've never been much for ceremony",
        "Saturn bar",
        "All the hory goats",
        "Jack be beanstalk",
        "Fanamlla hamburger",
        "Goldindo Holdintankers",]
    print(term.move(line,col) + screen)
    for line in outlines:
        print(term.bright_yellow(line))
        screen += term.bright_yellow(line) + "\n\r"
        time.sleep(0.01)

if __name__ == '__main__':
    main()
