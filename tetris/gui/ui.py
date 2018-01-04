import os, sys
import curses
import textwrap
from contextlib import contextmanager

from tetris.core import Game, Pos, Color
from tetris.gui.welcome import welcome_message
from tetris.gui.objects import *
from tetris.constants import TIME_INTERVAL, VERSION

from tetris import logger

class UI:
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
    def get_key(self, keys, delay=True, reactivity=10):
        if delay:
            self.stdscr.refresh()
            self.stdscr.nodelay(False)

        special = {
            'up': curses.KEY_UP,
            'down': curses.KEY_DOWN,
            'left': curses.KEY_LEFT,
            'right': curses.KEY_RIGHT,}
        keynum = lambda k: special[k] if k in special else ord(k)
        key_map = {keynum(k):k for k in keys}

        i, c = 0, self.stdscr.getch()
        while (delay and c not in key_map) or (not delay and i < reactivity):
            getched = self.stdscr.getch()
            if getched != -1:
                c = getched
            i += 1
        try:
            yield key_map.get(c, None)

        finally:
            if delay:
                self.stdscr.nodelay(True)

    def setup_colors(self):
        curses.start_color()
        self.has_colors = curses.has_colors()
        for color in Color:
            curses.init_pair(color.value, color.value, color.value)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.board_color = curses.color_pair(10)

    def doWelcome(self):
        self.stdscr.addstr(0, 0, welcome_message[0])
        blink = True
        animate_counter = 0
        refresh_counter = 0
        while True:
            with self.get_key(' ', delay=False) as key:
                if key == ' ':
                    return
            if refresh_counter % 10 == 0:
                self.stdscr.addstr(0, 0, welcome_message[animate_counter])
                animate_counter = (animate_counter + 1) % len(welcome_message)
                if blink:
                    Box().render(self)
                else:
                    Box("Press SPACEBAR to start!").render(self)
                blink = not blink
            refresh_counter += 1
            self.stdscr.addstr(23, 0, "{0} Eric Pai ©2014-2017".format(VERSION))
            curses.delay_output(10)
            self.stdscr.refresh()

    def gameLoop(self):
        while True:
            self.doRestart()
            while True:
                if self.g.has_ended:
                    self.doEnding("Game Over!")
                if self.has_landed:
                    self.g.new_piece()
                    self.has_landed = False
                else:
                    self.doMove()
                    if self.restart:
                        break
                    if not self.has_landed and self.down_counter == self.down_constant or self.fast_fall:  # do fall
                        self.has_landed = self.g.fall_piece()
                        self.down_counter = 1
                        self.fast_fall = False
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
        keys = 'up,down,left,right,p,q, '.split(',')
        with self.get_key(keys, delay=False) as key:
            if key == 'down': # moves piece down faster
                self.fast_fall = True
                curses.delay_output(self.time)
                if not self.has_landed:
                    self.has_landed = self.g.fall_piece()
                    self.displayBoard()
                if self.has_landed:
                    self.fast_fall = False
                    self.down_counter = 1
            elif key == 'left': # moves blocks to the left
                self.g.move_piece('left')
            elif key == 'right': # moves piece to the right
                self.g.move_piece('right')
            elif key == 'up': # rotates piece
                self.g.rotate_piece()
            elif key == 'p':
                self.doPause()
            elif key == ' ': # if spacebar, immediately drop to bottom
                self.g.drop_piece()
                self.has_landed = True
            elif key == 'q':
                self.doQuit()

    def doPause(self):
        dialog = Dialog("GAME PAUSED",
            """
                     Rotate piece
                          ^
                          |
            Move left <--   --> Move right
                          |
                          V
                      Fall faster
            """,
            '`spacebar` == Drop Piece',
            p='resume', q='quit', r='restart')

        with dialog.response(self) as key:
            if key == 'q':
                self.doQuit()
            if key == 'r':
                self.restart = True

    def refreshAnimation(self):
        self.stdscr.clear()
        curses.delay_output(self.time) # change so updates in real time
        self.down_counter += 1
        self.displayBoard()
        left = 28
        # score
        Box("level: {}".format(self.g.level), "lines: {}".format(self.g.cleared_lines),
            min_width=18
        ).render(self, pos=Pos(11, left))
        Box("score", '{} pts'.format(self.g.score),
            min_width=18
        ).render(self, pos=Pos(19, left))
        # next piece box
        Box(min_width=18, min_height=6).render(self, pos=Pos(2, left))
        nextPieceLines = self.g.next_piece.to_lines()
        for i, line in enumerate(nextPieceLines):
            for j, ch in enumerate(line):
                if ch.isdigit():
                    self.stdscr.addstr(i + 4, left + 7 + j, ch, curses.color_pair(int(ch)))
        Box("Next Piece", min_width=18, min_height=0).render(self, pos=Pos(1, left))
        # increment level
        if self.g.cleared_lines - self.level_constant*self.g.level >= 0:
            self.down_constant -= self.level_decrement
            self.g.level += 1
            if self.g.level == 11:
                self.doEnding('You Win!')
        self.stdscr.refresh()

    def doEnding(self, end_text):
        Box(end_text).render(self)
        self.stdscr.refresh()
        curses.delay_output(1500)
        score = "Score: {:,}".format(self.g.score)
        Box("Score: {:,}".format(self.g.score)).render(self)
        self.stdscr.refresh()
        curses.delay_output(1500)
        dialog = Dialog("Play again?", score, y='play again', n='quit')
        with dialog.response(self) as key:
            if key == 'n':
                raise ZeroDivisionError

    def doQuit(self):
        dialog = Dialog("Are you sure you want to quit?", y='quit', n='not')
        with dialog.response(self) as key:
            if key == 'y':
                raise ZeroDivisionError

    def doRestart(self):
        self.g = Game()
        self.time = 5
        self.fast_fall = False
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




