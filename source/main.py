import curses
from curses import wrapper
import time
from pathlib import Path
import random


ESCAP = False

def start_screen(stdscr):
    global ESCAP

    stdscr.clear()
    stdscr.addstr('Welcome to the Test Typing speed!')
    stdscr.addstr('\nPress any key to begin')
    stdscr.refresh()
    key = stdscr.getkey()
    try:
        if ord(key) == 27:
            ESCAP = True
    except:
        pass


def get_randomly_text():
    with open('texts.txt', 'r') as file_texts:
        texts = file_texts.readlines()
        target_text = random.choice(texts).strip()
    return target_text

def display_text(stdscr, target_text, current_text, wpm=0):
    stdscr.addstr(target_text)
    stdscr.addstr(1, 0 ,'WPM: {}'.format(wpm))

    for i, char in enumerate(current_text):
        correct_char = target_text[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0 , i, char, color)

def wpm_test(stdscr):
    global ESCAP
    # the tagret text user have to type that
    target_text = get_randomly_text()

    # the user's texts that clicked!
    current_text = []

    # wpm stuff
    wpm = 0
    start_time = time.time()

    stdscr.nodelay(True)

    # clean the shell
    stdscr.clear()
    stdscr.addstr(target_text)

    while True:
        # calculate the wpm
        time_elapsed = time.time() - start_time
        wpm = round(len(current_text) / (time_elapsed / 60) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        joined_text = ''.join(current_text)
        if joined_text == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey() # start typing here!
        except:
            continue 
        # escape of program
        try:
            if ord(key) == 27:
                ESCAP = True
                break
        except:
            pass
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)



def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    if not ESCAP:    
        while True:
            wpm_test(stdscr)
            if not ESCAP:
                stdscr.addstr(2, 0 ,'You completed the text. Press any key to continue...')
                stdscr.nodelay(False)
                key = stdscr.getkey()
                try:
                    if ord(key) == 27:
                        break
                except:
                    continue
            else:
                break

wrapper(main)

