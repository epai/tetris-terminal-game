import os
import sys
import curses
import textwrap
from contextlib import contextmanager

from tetris.game import *
from tetris.welcome import *
from tetris import setup
from tetris.constants import TIME_INTERVAL, VERSION

def clean_and_split(string):
    lines = textwrap.dedent(string.strip()).splitlines()
    return [l.strip() for l in lines if l.strip()]

class Box:
    def __init__(self, min_height=3, min_width=34):
        self.min_height = min_height
        self.min_width = min_width
        self.lines = []

    def add_text(self, text, padding_top=1):
        if not self.lines:
            padding_top = 0
        lines = clean_and_split(text)
        self.lines.extend(('',) * padding_top)
        self.lines.extend(lines)
        longest_line = max(len(line) for line in lines)
        self.min_width = max(self.min_width, longest_line)
        return self

    def render(self, ui):
        actual_height = len(self.lines)
        padding = max(0, self.min_height - actual_height)

        pad = '|{}|\n'.format(' '*self.min_width)
        middle = '\n'.join('|{}|'.format(l.center(self.min_width)) for l in self.lines)

        box_lines = clean_and_split("""
        ┌{center}┐
        {padding}
        {middle}
        {padding}
        {extra}
        └{center}┘
        """.format(
            center='-'*self.min_width,
            padding=pad * (padding // 2),
            extra=pad if padding % 2 == 1 else '',
            middle=middle)
        )

        box_height = max(self.min_height, actual_height)
        box_width = self.min_width + 2
        pos = setup.Pos(
            ui.height // 2 - box_height // 2,
            ui.width // 2 - box_width // 2)

        for offset, line in enumerate(box_lines):
            ui.stdscr.addstr(pos.y + offset, pos.x, line)


class UI:
    nextPieceBoarder = \
    ("┌------------------┐\n",
     "|    Next Piece    |\n",
     "|==================|\n",
     "|                  |\n",
     "|                  |\n",
     "|                  |\n",
     "|                  |\n",
     "|                  |\n",
     "|                  |\n",
     "└------------------┘\n")

    def __init__(self):
        # setup curses
        self.stdscr = curses.initscr()
        self.setup_colors()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)
        # initialize game params
        self.doRestart()
        self.height, self.width = \
                [int(x) for x in os.popen('stty size', 'r').read().split()]

    @contextmanager
    def get_key(self, keys, delay=True):
        if delay:
            self.stdscr.refresh()
            self.stdscr.nodelay(False)

        special = {
            'up': curses.KEY_LEFT,
            'down': curses.KEY_DOWN,
            'left': curses.KEY_LEFT,
            'right': curses.KEY_RIGHT,}
        keynum = lambda k: special[k] if k in special else ord(k)
        key_map = {keynum(k):k for k in keys}

        c = self.stdscr.getch()
        while delay and c not in key_map:
            c = self.stdscr.getch()
        try:
            yield key_map.get(c, None)

        finally:
            if delay:
                self.stdscr.nodelay(True)

    def setup_colors(self):
        curses.start_color()
        self.has_colors = curses.has_colors()
        for color in setup.Color:
            curses.init_pair(color.value, color.value, color.value)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.board_color = curses.color_pair(10)

    def doWelcome(self):
        self.stdscr.addstr(0, 0, welcomeMessage[0])
        start = False
        blink_counter = 1
        blink = True
        animate_counter = 0
        refresh_counter = 10
        while (not start):
            for i in range(1000):
                with self.get_key(' ', delay=False) as key:
                    if key == ' ':
                        start = True
                        break
            if refresh_counter == 10:
                refresh_counter = 1
                if animate_counter == len(welcomeMessage):
                    animate_counter = 0
                self.stdscr.addstr(0, 0, welcomeMessage[animate_counter])
                animate_counter += 1
                if blink:
                    Box().render(self)
                else:
                    Box().add_text("Press SPACEBAR to start!").render(self)
                blink = not blink
                blink_counter = 0
            refresh_counter += 1
            self.stdscr.addstr(23, 0, "{0} Eric Pai ©2014".format(VERSION))
            curses.delay_output(5)
            blink_counter += 1
            self.stdscr.refresh()

    def gameLoop(self):
        while True:
            self.doRestart()
            while True:
                if self.g.has_ended:
                    self.doGameOver()
                if self.has_landed:
                    self.g.new_piece()
                    self.has_landed = False
                else:
                    self.doMove()
                    if self.restart:
                        break
                    if not self.has_landed and \
                           self.down_counter == self.down_constant:  # do fall
                        self.has_landed = self.g.fall_piece()
                        self.down_counter = 1
                self.refreshAnimation()

    def displayBoard(self):
        board_string = str(self.g)
        if not self.has_colors:
            self.stdscr.addstr(0, 0, board_string)
            return
        for y, line in enumerate(board_string.splitlines()):
            for x, ch in enumerate(line):
                if ch.isdigit():
                    color = int(ch)
                    if color == 9:
                        self.stdscr.addstr(y, x, '░', self.board_color)
                    else:
                        self.stdscr.addstr(y, x, ch, curses.color_pair(color))
                else:
                    self.stdscr.addstr(y, x, ch, self.board_color)

    def doMove(self):
        last_move = 0
        keys = 'up,down,left,right,p,q, '.split(',')
        for i in range(1000):  # improves reactivity
            with self.get_key(keys, delay=False) as key:
                if key == 'down': # moves piece down faster
                    self.down_counter = self.down_constant
                    curses.delay_output(self.time)
                    if not self.has_landed:
                        self.has_landed = self.g.fall_piece()
                        self.displayBoard()
                    if self.has_landed:
                        self.down_counter = 1
                elif key == 'left': # moves blocks to the left
                    last_move = -1
                elif key == 'right': # moves piece to the right
                    last_move = 1
                elif key == 'up': # rotates piece
                    self.g.rotate_piece()
                elif key == 'p':
                    self.doPause()
                elif key == ' ': # if spacebar, immediately drop to bottom
                    self.g.drop_piece()
                    self.has_landed = True
                    break
                elif key == 'q':
                    self.doQuit()
                    self.down_counter = 1
        self.g.move_piece(last_move)

    def doPause(self):
        def printMenu():
            (Box()
                .add_text("GAME PAUSED")
                .add_text(
                    """
                             Rotate piece
                                  ^
                                  |
                    Move left <--   --> Move right
                                  |
                                  V
                              Fall faster
                    """)
                .add_text(
                    """
                    Type `p` to resume
                         `q` to quit
                         `r` to restart
                         `spacebar` to drop
                    """)
            ).render(self)
            self.stdscr.refresh()
        printMenu()
        with self.get_key('qr') as key:
            if key == 'q':
                self.doQuit()
                printMenu()
            if key == 'r':
                self.restart = True

    def refreshAnimation(self):
        self.stdscr.clear()
        curses.delay_output(self.time) # change so updates in real time
        self.down_counter += 1
        self.displayBoard()
        # score
        self.stdscr.addstr(20, 52, "lines completed: {0}".format(self.g.cleared_lines))
        self.stdscr.addstr(22, 42, "Type 'q' to quit or 'p' for pause.")
        self.stdscr.addstr(15, 52, "level: {0}".format(self.g.level))
        self.stdscr.addstr(17, 48, "--------------------------")
        self.stdscr.addstr(18, 48, "    Score {:,}             ".format(self.g.score))
        self.stdscr.addstr(19, 48, "--------------------------")
        # next piece box
        for i in range(len(self.nextPieceBoarder)):
            self.stdscr.addstr(i + 1, 49, self.nextPieceBoarder[i])
        nextPieceLines = self.g.next_piece.to_lines()
        for i, line in enumerate(nextPieceLines):
            for j, ch in enumerate(line):
                if ch.isdigit():
                    color = int(ch)
                    self.stdscr.addstr(i + 5, 56 + j, ch, curses.color_pair(color))
                else:
                    self.stdscr.addstr(i + 5, 56 + j, ch, self.board_color)
        if self.g.cleared_lines - self.level_constant*self.g.level >= 0:
            self.down_constant -= self.level_decrement
            self.g.level += 1
            if self.g.level == 11:
                self.doWin()

    def doGameOver(self):
        Box().add_text("Game Over!").render(self)
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(13, 24, "|         Score:  {:,}".format(self.g.score))
        self.stdscr.refresh()
        curses.delay_output(1500)
        (Box()
            .add_text("Play again?")
            .add_text("`y` for yes, `n` for no")
        ).render(self)
        with self.get_key('yn') as key:
            if key == 'n':
                raise ZeroDivisionError

    def doWin(self):
        Box().add_text("You win!").render(self)
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(12, 24, "|         Score:  {:,}".format(self.g.score))
        self.stdscr.refresh()
        curses.delay_output(1500)
        (Box()
            .add_text("Play again?")
            .add_text("`y` for yes, `n` for no")
        ).render(self)
        with self.get_key('yn') as key:
            if key == 'n':
                raise ZeroDivisionError

    def doQuit(self):
        (Box()
            .add_text("Are you sure you want to quit?")
            .add_text("`y` for yes, `n` for no")
        ).render(self)
        with self.get_key('yn') as key:
            if key == 'y':
                raise ZeroDivisionError

    def doRestart(self):
        self.g = Game()
        self.time = 5
        self.has_landed = True
        self.down_counter = 1
        self.down_constant = 100
        self.level_constant = 5
        self.level_decrement = 10
        self.restart = False

    def doFinish(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()




