# Eric Pai
# Spring 2014

""" Includes all supporting data structures used by game.py """

class Position:
	def __init__(self, row, column):
		self.row = row
		self.col = column

class Tetrimino:
	def __init__(self, shape, topLeft=Position(0, 0)):
		self.shape = shape
		self.originShape = shape
		self.topLeft = topLeft
		self.rotations = {}
		self.currRotation = 0; # index of current rotation

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

	def setRotations(self, rotations):
		""" takes in a set of rotations (as tuples) and sets them. """
		for i in range(len(rotations)):
			self.rotations[i] = rotations[i]

	def getNextRotation(self):
		temp = self.rotations[self.currRotation]
		self.currRotation = (self.currRotation + 1) % len(self.rotations)
		return temp


class Pieces:
	""" Uses the Nintendo Rotation system for rotations.
		http://tetris.wikia.com/wiki/
		Nintendo_Rotation_System?file=NESTetris-pieces.png"""
	I = Tetrimino(\
		((0, 1, 0, 0),
		(0, 1, 0, 0),
		(0, 1, 0, 0),
		(0, 1, 0, 0)))
	I_rotations = \
		(
			(
			(0, 0, 0, 0),
			(0, 0, 0, 0),
			(1, 1, 1, 1),
			(0, 0, 0, 0)),
			(
			(0, 1, 0, 0),
			(0, 1, 0, 0),
			(0, 1, 0, 0),
			(0, 1, 0, 0))
		)
	I.setRotations(I_rotations)

	J = Tetrimino(\
		((0, 0, 0),
		(2, 2, 2),
		(0, 0, 2)))
	J_rotations = \
		(
			(
			(0, 2, 0),
			(0, 2, 0),
			(2, 2, 0)),
			(
			(2, 0, 0),
			(2, 2, 2),
			(0, 0, 0)),
			(
			(0, 2, 2),
			(0, 2, 0),
			(0, 2, 0)),
			(
			(0, 0, 0),
			(2, 2, 2),
			(0, 0, 2))
		)
	J.setRotations(J_rotations)

	L = Tetrimino(\
		((0, 0, 0),
		(3, 3, 3),
		(3, 0, 0)))
	L_rotations = \
		(
			(
			(3, 3, 0),
			(0, 3, 0),
			(0, 3, 0)),
			(
			(0, 0, 3),
			(3, 3, 3),
			(0, 0, 0)),
			(
			(0, 3, 0),
			(0, 3, 0),
			(0, 3, 3)),
			(
			(0, 0, 0),
			(3, 3, 3),
			(3, 0, 0))
		)
	L.setRotations(L_rotations)

	O = Tetrimino(\
		((0, 0, 0, 0),
		(0, 4, 4, 0),
		(0, 4, 4, 0),
		(0, 0, 0, 0)))
	O_rotations = \
		((
			(0, 0, 0, 0),
			(0, 4, 4, 0),
			(0, 4, 4, 0),
			(0, 0, 0, 0)),)
	O.setRotations(O_rotations)

	S = Tetrimino(\
		((0, 0, 0),
		(0, 5, 5),
		(5, 5, 0)))
	S_rotations = \
		(
			(
			(0, 5, 0),
			(0, 5, 5),
			(0, 0, 5)),
			(
			(0, 0, 0),
			(0, 5, 5),
			(5, 5, 0))
		)
	S.setRotations(S_rotations)

	T = Tetrimino(\
		((0, 0, 0),
		(6, 6, 6),
		(0, 6, 0)))
	T_rotations = \
		(
			(
			(0, 6, 0),
			(6, 6, 0),
			(0, 6, 0)),
			(
			(0, 6, 0),
			(6, 6, 6),
			(0, 0, 0)),
			(
			(0, 6, 0),
			(0, 6, 6),
			(0, 6, 0)),
			(
			(0, 0, 0),
			(6, 6, 6),
			(0, 6, 0))
		)
	T.setRotations(T_rotations)

	Z = Tetrimino(\
		((0, 0, 0),
		(7, 7, 0),
		(0, 7, 7)))
	Z_rotations = \
		(
			(
			(0, 0, 7),
			(0, 7, 7),
			(0, 7, 0)),
			(
			(0, 0, 0),
			(7, 7, 0),
			(0, 7, 7))
		)
	Z.setRotations(Z_rotations)

	pieces = {1 : I, 2 : J, 3 : L, 4 : O, 5 : S, 6 : T, 7 : Z}

	num_pieces = len(pieces)

	def getPiece(self, num):
		""" Takes in a piece number and returns the corresponding piece. """
		return Pieces.pieces[num]

