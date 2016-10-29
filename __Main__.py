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
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
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

    def addstr(x, y, msg):
        self.stdscrn.addstr(x, y, msg, curses.color_pair(1))

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
        # self.stdscr.clear()
        # self.stdscr.refresh()
        # self.stdscr.addstr(11, 22, "ready ...")
        # self.stdscr.refresh()
        # curses.delay_output(500)
        # self.stdscr.addstr(11, 32, "set ...")
        # self.stdscr.refresh()
        # curses.delay_output(500)
        # self.stdscr.addstr(9, 40,  "┌-----------┐")
        # self.stdscr.addstr(10, 40, "|           |")
        # self.stdscr.addstr(11, 40, "|    GO!    |")
        # self.stdscr.addstr(12, 40, "|           |")
        # self.stdscr.addstr(13, 40, "└-----------┘")
        # self.stdscr.refresh()
        # curses.delay_output(500)

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
                    self.g.updateBoard()
                    self.stdscr.addstr(0, 0, self.g.toString())
                if self.has_landed:
                    self.down_counter = 1
            if c == curses.KEY_LEFT: # moves blocks to the left
                last_move = -1
            elif c == curses.KEY_RIGHT: # moves piece to the right
                last_move = 1
            elif not shape_change and c == curses.KEY_UP: # rotates piece
                self.g.rotatePiece()
                shape_change = True
            elif c == ord('m'):
                self.doMenu()
            elif c == ord('q'):
                self.doQuit()
            elif c == ord('p'):
                self.doPause()
        self.g.movePiece(last_move)

    def doMenu(self):
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
            self.stdscr.addstr(15, 24, "|    Type 'm' to resume,         |")
            self.stdscr.addstr(16, 24, "|         'q' to quit            |")
            self.stdscr.addstr(17, 24, "|         'r' to restart         |")
            self.stdscr.addstr(18, 24, "└--------------------------------┘")
            self.stdscr.refresh()
        printMenu()
        self.stdscr.nodelay(False)
        c = self.stdscr.getch()
        while c not in (ord('q'), ord('r'), ord('m')):
            c = self.stdscr.getch()
        if c == ord('q'):
            self.doQuit()
            printMenu()
        if c == ord('r'):
            self.restart = True
        self.stdscr.nodelay(True)

    def doPause(self):
        self.stdscr.addstr(9, 22, "┌----------------------------┐")
        self.stdscr.addstr(10, 22, "|                            |")
        self.stdscr.addstr(11, 22, "|       Game is Paused       |")
        self.stdscr.addstr(12, 22, "|    press 'p' to unpause    |")
        self.stdscr.addstr(13, 22, "|                            |")
        self.stdscr.addstr(14, 22, "└----------------------------┘")
        self.stdscr.nodelay(False)
        c = self.stdscr.getch()
        while c != ord('p'):
            c = self.stdscr.getch()
        self.stdscr.nodelay(True)

    def refreshAnimation(self):
        curses.delay_output(self.time) # change so updates in real time
        self.down_counter += 1
        self.stdscr.addstr(0, 0, self.g.toString())
        # score
        self.stdscr.addstr(20, 52, "lines completed: {0}".format(self.g.clearedLines))
        self.stdscr.addstr(22, 42, "Type 'q' to quit, 'm' for menu,")
        self.stdscr.addstr(23, 52, "'p' to pause.")
        self.stdscr.addstr(15, 52, "level: {0}".format(self.g.level))
        self.stdscr.addstr(17, 48, "--------------------------")
        self.stdscr.addstr(18, 48, "    Score {:,}             ".format(self.g.score))
        self.stdscr.addstr(19, 48, "--------------------------")
        # next piece box
        for i in range(len(self.nextPieceBoarder)):
            self.stdscr.addstr(i + 1, 49, self.nextPieceBoarder[i])
        nextPieceLines = self.g.nextPieceToString()
        for i in range(len(nextPieceLines)):
            self.stdscr.addstr(i + 5, 53, nextPieceLines[i])
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




