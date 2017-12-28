# Eric Pai
# Spring 2014

""" Includes all supporting data structures used by game.py """

class Position:
	def __init__(self, row, column):
		self.row = row
		self.col = column
	def __str__(self):
		return '({},{})'.format(self.row, self.col)

class Tetrimino:
	def __init__(self, color, shape, topLeft=Position(0, 0)):
		self.color = color
		self.shape = shape
		self.originShape = shape
		self.topLeft = topLeft
		self.currRotation = 0; # index of current rotation
		self.rotations = self.getRotations(shape)

	def getWidth(self):
		return len(self.shape[0])

	def getHeight(self):
		return len(self.shape)

	def getNextFall(self):
		return Position(self.topLeft.row + 1, self.topLeft.col)

	def getNextRight(self):
		return Position(self.topLeft.row, self.topLeft.col + 1)

	def getNextLeft(self):
		return Position(self.topLeft.row, self.topLeft.col - 1)

	def getRotations(self, shape):
		""" takes in a set of rotations (as tuples) and sets them. """
		currRotation = shape
		rotations = []
		for _ in range(len(shape)):
			reversedRotation = currRotation[::-1]
			currRotation = [[row[i] for row in reversedRotation]
					for i in range(len(shape))]
			rotations.append(currRotation)
		rotations.append(shape)
		return rotations

	def getNextRotation(self):
		temp = self.rotations[self.currRotation]
		self.currRotation = (self.currRotation + 1) % len(self.rotations)
		return temp

def makePieces():
	raw_pieces = \
	"""
	.X..
	.X..
	.X..
	.X..

	...
	XXX
	..X

	...
	XXX
	X..

	....
	.XX.
	.XX.
	....

	...
	.XX
	XX.

	...
	XXX
	.X.

	...
	XX.
	.XX
	"""
	pieces = [(i+1, [[i + 1 if ch == 'X' else 0 for ch in row.strip()]
				for row in piece.split('\n') if row.strip()])
				for i, piece in enumerate(raw_pieces.split('\n\n'))]
	pieces = [Tetrimino(color, piece) for color, piece in pieces]
	pieces[0].rotations = pieces[0].rotations[:2] # L piece
	pieces[3].rotations = pieces[3].rotations[:1] # O piece
	pieces[4].rotations = pieces[4].rotations[:2] # s piece
	pieces[6].rotations = pieces[6].rotations[:2] # z piece
	return pieces







