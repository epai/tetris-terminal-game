# Eric Pai
# Spring 2014

import os
import sys
import curses
#import locale
from __game__ import *
from __welcome__ import *

class Main:
    ### FIELDS and SETUP ###
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
    ########################

    def __init__(self):
        self.version = 0.92
        ### curses setup ###
        self.stdscr = curses.initscr()
        self.setupColors()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)
        ### Field Variables ###
        #  -- initialized in self.doRestart() -- #
        self.doRestart()
        ### other ###
        self.rows, self.columns = \
                [int(x) for x in os.popen('stty size', 'r').read().split()]

    def setupColors(self):
        curses.start_color()
        self.has_colors = curses.has_colors()
        if self.has_colors:
            colors = [
                curses.COLOR_RED,
                curses.COLOR_YELLOW,
                curses.COLOR_MAGENTA,
                curses.COLOR_BLUE,
                curses.COLOR_CYAN,
                curses.COLOR_GREEN,
                curses.COLOR_WHITE,
            ]
            for i, color in enumerate(colors):
                curses.init_pair(i + 1, color, color)
            curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
            self.boardColor = curses.color_pair(10)

    def doWelcome(self):
        self.stdscr.addstr(0, 0, welcomeMessage[0])
        start = False
        blink_counter = 1
        blink = True
        animate_counter = 0
        refresh_counter = 10
        while (not start):
            c = self.stdscr.getch()
            for i in range(10000):
                c = self.stdscr.getch()
                if c != -1:
                    start = True
                    break
            if refresh_counter == 10:
                refresh_counter = 1
                if animate_counter == len(welcomeMessage):
                    animate_counter = 0
                self.stdscr.addstr(0, 0, welcomeMessage[animate_counter])
                animate_counter += 1
                if blink:
                    self.stdscr.addstr(14, 22, "┌--------------------------------┐")
                    self.stdscr.addstr(15, 22, "|                                |")
                    self.stdscr.addstr(16, 22, "|                                |")
                    self.stdscr.addstr(17, 22, "|                                |")
                    self.stdscr.addstr(18, 22, "└--------------------------------┘")
                else:
                    self.stdscr.addstr(14, 22, "┌--------------------------------┐")
                    self.stdscr.addstr(15, 22, "|                                |")
                    self.stdscr.addstr(16, 22, "|     Press ANY key to start!    |")
                    self.stdscr.addstr(17, 22, "|                                |")
                    self.stdscr.addstr(18, 22, "└--------------------------------┘")
                blink = not blink
                blink_counter = 0
            refresh_counter += 1
            #self.stdscr.addstr(23, 70, "Eric Pai")
            self.stdscr.addstr(23, 0, "v{0} Eric Pai ©2014".format(self.version))
            curses.delay_output(5)
            blink_counter += 1
            self.stdscr.refresh()

    def gameLoop(self):
        while True:
            self.doRestart()
            while True:
                if self.g.gameOver:
                    self.doGameOver()
                if self.has_landed:
                    self.g.newPiece()
                    self.has_landed = False
                else:
                    self.doMove()
                    if self.restart:
                        break
                    if not self.has_landed and \
                           self.down_counter == self.down_constant:  # do fall
                        self.has_landed = self.g.fallPiece()
                        self.down_counter = 1
                self.refreshAnimation()

    def displayBoard(self):
        boardString = self.g.toString()
        if not self.has_colors:
            self.stdscr.addstr(0, 0, self.g.toString())
            return
        for y, line in enumerate(boardString.split("\n")):
            for x, ch in enumerate(line):
                if ch.isdigit():
                    color = int(ch)
                    if color == 9:
                        self.stdscr.addstr(y, x, '░', self.boardColor)
                    else:
                        self.stdscr.addstr(y, x, ch, curses.color_pair(color))
                else:
                    self.stdscr.addstr(y, x, ch, self.boardColor)

    def doMove(self):
        last_move = 0
        shape_change = False
        for i in range(1000):  # improves reactivity
            c = self.stdscr.getch()
            if c == curses.KEY_DOWN: # moves piece down faster
                self.down_counter = self.down_constant
                curses.delay_output(self.time)
                if not self.has_landed:
                    self.has_landed = self.g.fallPiece()
                    self.displayBoard()
                if self.has_landed:
                    self.down_counter = 1
            if c == curses.KEY_LEFT: # moves blocks to the left
                last_move = -1
            elif c == curses.KEY_RIGHT: # moves piece to the right
                last_move = 1
            elif not shape_change and c == curses.KEY_UP: # rotates piece
                self.g.rotatePiece()
                shape_change = True
            elif c == ord('p'):
                self.doPause()
            elif c == ord(' '): # if spacebar, immediately drop to bottom
                self.g.dropPiece()
                self.has_landed = True
                break
            elif c == ord('q'):
                self.doQuit()
                self.down_counter = 1
        self.g.movePiece(last_move)

    def doPause(self):
        def printMenu():
            self.stdscr.addstr(5, 24,  "┌--------------------------------┐")
            self.stdscr.addstr(6, 24,  "|           GAME PAUSED          |")
            self.stdscr.addstr(7, 24,  "|                                |")
            self.stdscr.addstr(8, 24,  "| Controls:                      |")
            self.stdscr.addstr(9, 24,  "|               ^ Rotate Piece   |")
            self.stdscr.addstr(10, 24, "|               |                |")
            self.stdscr.addstr(11, 24, "| Move left <--   --> Move right |")
            self.stdscr.addstr(12, 24, "|               |                |")
            self.stdscr.addstr(13, 24, "|               V Fall faster    |")
            self.stdscr.addstr(14, 24, "|                                |")
            self.stdscr.addstr(15, 24, "|    Type 'p' to resume,         |")
            self.stdscr.addstr(16, 24, "|         'q' to quit            |")
            self.stdscr.addstr(17, 24, "|         'r' to restart         |")
            self.stdscr.addstr(18, 24, "└--------------------------------┘")
            self.stdscr.refresh()
        printMenu()
        self.stdscr.nodelay(False)
        c = self.stdscr.getch()
        while c not in (ord('q'), ord('r'), ord('p')):
            c = self.stdscr.getch()
        if c == ord('q'):
            self.doQuit()
            printMenu()
        if c == ord('r'):
            self.restart = True
        self.stdscr.nodelay(True)

    def refreshAnimation(self):
        self.stdscr.clear()
        curses.delay_output(self.time) # change so updates in real time
        self.down_counter += 1
        self.displayBoard()
        # score
        self.stdscr.addstr(20, 52, "lines completed: {0}".format(self.g.clearedLines))
        self.stdscr.addstr(22, 42, "Type 'q' to quit or 'p' for pause.")
        self.stdscr.addstr(15, 52, "level: {0}".format(self.g.level))
        self.stdscr.addstr(17, 48, "--------------------------")
        self.stdscr.addstr(18, 48, "    Score {:,}             ".format(self.g.score))
        self.stdscr.addstr(19, 48, "--------------------------")
        # next piece box
        for i in range(len(self.nextPieceBoarder)):
            self.stdscr.addstr(i + 1, 49, self.nextPieceBoarder[i])
        nextPieceLines = self.g.nextPieceToString()
        for i, line in enumerate(nextPieceLines):
            for j, ch in enumerate(line):
                if ch.isdigit():
                    color = int(ch)
                    self.stdscr.addstr(i + 5, 56 + j, ch, curses.color_pair(color))
                else:
                    self.stdscr.addstr(i + 5, 56 + j, ch, self.boardColor)
        if self.g.clearedLines - self.level_constant*self.g.level >= 0:
            self.down_constant -= self.level_decrement
            self.g.level += 1
            if self.g.level == 11:
                self.doWin()

    def doGameOver(self):
        #self.stdscr.clear()
        #self.stdscr.addstr(11, 34, "Game Over!")

        self.stdscr.addstr(10, 24, "┌--------------------------------┐")
        self.stdscr.addstr(11, 24, "|                                |")
        self.stdscr.addstr(12, 24, "|           Game Over!           |")
        self.stdscr.addstr(13, 24, "|                                |")
        self.stdscr.addstr(14, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(12, 24, "|         Score:  {:,}".format(self.g.score))
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(9, 24, "┌--------------------------------┐")
        self.stdscr.addstr(10, 24, "|           Play again?          |")
        self.stdscr.addstr(11, 24, "|                                |")
        self.stdscr.addstr(13, 24, "|                                |")
        self.stdscr.addstr(14, 24, "|     'y' for yes, 'n' for no    |")
        self.stdscr.addstr(15, 24, "└--------------------------------┘")
        # self.stdscr.addstr(11, 27, "       Play again?     ")
        # self.stdscr.addstr(13, 27, "'y' for yes, 'n' for no")
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        c = self.stdscr.getch()
        while c not in (ord('y'), ord('n')):
            c = self.stdscr.getch()
        if c == ord('y'):
            self.restart = True
        if not self.restart:
            raise ZeroDivisionError
        self.stdscr.nodelay(True)

    def doWin(self):
        #self.stdscr.clear()
        self.stdscr.addstr(10, 24, "┌--------------------------------┐")
        self.stdscr.addstr(11, 24, "|                                |")
        self.stdscr.addstr(12, 24, "|            You win!            |")
        self.stdscr.addstr(13, 24, "|                                |")
        self.stdscr.addstr(14, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(12, 24, "|         Score:  {:,}".format(self.g.score))
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(10, 24, "┌--------------------------------┐")
        self.stdscr.addstr(11, 24, "|           Play again?          |")
        self.stdscr.addstr(11, 24, "|                                |")
        self.stdscr.addstr(13, 24, "|                                |")
        self.stdscr.addstr(13, 24, "|     'y' for yes, 'n' for no    |")
        self.stdscr.addstr(14, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        c = self.stdscr.getch()
        while c not in (ord('y'), ord('n')):
            c = self.stdscr.getch()
        if c == ord('y'):
            self.restart = True
        if not self.restart:
            raise ZeroDivisionError
        self.stdscr.nodelay(True)

    def doQuit(self):
        self.stdscr.addstr(10, 24, "┌--------------------------------┐")
        self.stdscr.addstr(11, 24, "| Are you sure you want to quit? |")
        self.stdscr.addstr(12, 24, "|                                |")
        self.stdscr.addstr(13, 24, "|    'y' for yes, 'n' for no     |")
        self.stdscr.addstr(14, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        c = self.stdscr.getch()
        while c not in (ord('y'), ord('n')):
            c = self.stdscr.getch()
        if c == ord('y'):
            raise ZeroDivisionError

    def doRestart(self):
        self.time = 5
        self.g = Game()
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




