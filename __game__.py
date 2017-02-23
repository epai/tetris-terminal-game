# Eric Pai
# Spring 2014

""" Game Logic and internal representation for tetris.py """

### TO DO:  IMPLEMENT LANDING, IMPLEMENT COLLISION DETECTION,
###			IMPLEMENT LINE CLEARING

import random
from copy import deepcopy
from __setup__ import *

class RollDeck():
	def __init__(self, deck):
		self.originLength = len(deck)
		self.deck = []
		[self.deck.extend(deepcopy(deck)) for _ in range(3)] # make two copies of deck
		self.originalDeck = deepcopy(self.deck)
		random.shuffle(self.deck)

	def draw(self):
		card = self.deck.pop()
		if len(self.deck) < self.originLength:
			self.deck = self.originalDeck
			random.shuffle(self.deck)
		return card

class Game:
	TIME = 0.1

	def __init__(self, rows=23, columns=10):
		self.board = [[0 for c in range(columns)] for r in range(rows)]
		self.emptyBoard = deepcopy(self.board)
		self.landed = deepcopy(self.board)
		self.simulateLanded = deepcopy(self.board)
		self.gamePver = False
		self.currPiece = None
		self.clearedLines = 0
		self.pieces = makePieces()
		self.deck = RollDeck(self.pieces)
		self.nextPiece = self.deck.draw()
		self.gameOver = False
		self.clearLinesAnimation = None
		self.clearLinesBoolean = False
		self.score = 0
		self.level = 1

	def newPiece(self):
		self.currPiece = self.nextPiece
		self.nextPiece = self.deck.draw()
		if self.nextPiece == self.pieces[0]:
			self.currPiece.topLeft = Position(0, 4)
		else:
			self.currPiece.topLeft = Position(0, 3)
		p = self.currPiece
		for r in range(p.getHeight()):
			for c in range(p.getWidth()):
				if p.shape[r][c] != 0:
					row = r + p.topLeft.row
					col = c + p.topLeft.col
					if self.landed[row][col] != 0:
						self.gameOver = True
						return

	def simulateLand(self):
		currTopLeft = self.currPiece.getNextFall()
		rows = range(self.currPiece.getHeight())
		cols = range(self.currPiece.getWidth())
		landed = False
		while not landed:
			for r in rows:
				for c in cols:
					if self.currPiece.shape[r][c] != 0:
						row = r + currTopLeft.row
						col = c + currTopLeft.col
						if row >= len(self.landed) or self.landed[row][col] != 0:
							landed = True
							break
			if landed == True:
				break
			currTopLeft.row += 1
		shapeRows = range(self.currPiece.getHeight())
		shapeColumns = range(self.currPiece.getWidth())
		for r in shapeRows:
			for c in shapeColumns:
				if self.currPiece.shape[r][c] != 0:
					row = r + currTopLeft.row - 1
					col = c + currTopLeft.col
					self.simulateLanded[row][col] = self.currPiece.shape[r][c]


	def fallPiece(self):
		nextTopLeft = self.currPiece.getNextFall()
		p = self.currPiece
		tL = p.topLeft
		rows = range(p.getHeight())
		cols = range(p.getWidth())
		has_landed = False
		for r in rows:
			for c in cols:
				if p.shape[r][c] != 0:
					row = r + nextTopLeft.row
					col = c + nextTopLeft.col
					if row >= len(self.landed) or self.landed[row][col] != 0:
						self.landPiece()
						return True
		self.currPiece.topLeft = nextTopLeft
		return False

	def movePiece(self, dir):
		p = self.currPiece
		if dir == -1:
			nextTopLeft = p.getNextLeft()
		elif dir == 1:
			nextTopLeft = p.getNextRight()
		else:
			return
		rows = range(p.getHeight())
		cols = range(p.getWidth())
		for r in rows:
			for c in cols:
				if p.shape[r][c] != 0:
					row = r + nextTopLeft.row
					col = c + nextTopLeft.col
					if col < 0 or col >= len(self.landed[0]) \
							   or self.landed[row][col] != 0:
						return
		self.currPiece.topLeft = nextTopLeft

	def dropPiece(self):
		fallen = False
		while not fallen:
			fallen = self.fallPiece()

	def rotatePiece(self):
		p = self.currPiece
		topLeft = p.topLeft
		nextRotation = p.getNextRotation()
		rows = range(len(nextRotation))
		cols = range(len(nextRotation[0]))
		try:
			for r in rows:
				for c in cols:
					if nextRotation[r][c] != 0:
						row = r + topLeft.row
						col = c + topLeft.col
						if col < 0:
							self.movePiece(1)
							#return
						elif col >= len(self.landed[0]):
							self.movePiece(-1)
							#return
						elif self.landed[row][col] != 0:
							return
		except IndexError as e:
			return
		self.currPiece.shape = nextRotation

	def landPiece(self):
		p = self.currPiece
		shapeRows = range(self.currPiece.getHeight())
		shapeColumns = range(self.currPiece.getWidth())
		self.score += 400 * self.level
		for r in shapeRows:
			for c in shapeColumns:
				if self.currPiece.shape[r][c] != 0:
					row = r + self.currPiece.topLeft.row
					col = c + self.currPiece.topLeft.col
					self.landed[row][col] = self.currPiece.shape[r][c]
		self.clearLines()

	def clearLines(self):
		animation = []
		rows = range(len(self.landed))
		cols = range(len(self.landed[0]))
		score = 0
		combo = 0
		for row in rows:
			isFilled = True
			for col in cols:
				if self.landed[row][col] == 0:
					isFilled = False
			if isFilled:
				empty = [0]*len(self.landed[0])
				self.landed = [empty] + self.landed[:row] + self.landed[row+1:]
				self.clearedLines += 1
				score += len(self.board[0]) * self.level * 1000
				combo += 1
		self.score += score * combo

	def updateBoard(self):
		""" Updates board to include landed[] and curr tetrimino piece """
		self.board = deepcopy(self.emptyBoard)
		self.simulateLanded = deepcopy(self.emptyBoard)
		self.simulateLand()
		rows = range(len(self.board))
		columns = range(len(self.board[0]))
		shapeRows = range(self.currPiece.getHeight())
		shapeColumns = range(self.currPiece.getWidth())
		for r in rows:
			for c in columns:
				self.board[r][c] = self.landed[r][c]
				if self.simulateLanded[r][c]:
					self.board[r][c] = 9
		for r in shapeRows:
			for c in shapeColumns:
				if self.currPiece.shape[r][c] != 0:
					row = r + self.currPiece.topLeft.row
					col = c + self.currPiece.topLeft.col
					self.board[row][col] = self.currPiece.shape[r][c]

	def toString(self):
		rows = len(self.board)
		cols = len(self.board[0])
		result = ".." * (cols + 2) + "\n"
		self.updateBoard()
		for r in range(1, rows):
			result += "||"
			for c in range(cols):
				if self.board[r][c] != 0:
					result += "{0}{0}".format(self.board[r][c])
				else:
					result += "  "
			result += "||\n"
		result += "^^" * (cols + 2)
		return result

	def nextPieceToString(self):
		result = []
		shapeRows = range(self.nextPiece.getHeight())
		shapeColumns = range(self.nextPiece.getWidth())
		for r in shapeRows:
			line = ""
			for c in shapeColumns:
				if self.nextPiece.originShape[r][c] == 0:
					line += "  "
				else:
					line += "{0}{0}".format(self.nextPiece.originShape[r][c])
			result += [line]
		return result
