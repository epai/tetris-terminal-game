import enum
import random
import curses
from textwrap import dedent

class Pos:
	def __init__(self, y, x):
		self.row = self.y = y
		self.col = self.x = x

	def __str__(self):
		return '({},{})'.format(self.y, self.x)

	def __iter__(self):
		return iter((self.row, self.col))

@enum.unique
class Color(enum.Enum):
	RED = curses.COLOR_RED
	YELLOW = curses.COLOR_YELLOW
	MAGENTA = curses.COLOR_MAGENTA
	BLUE = curses.COLOR_BLUE
	CYAN = curses.COLOR_CYAN
	GREEN = curses.COLOR_GREEN
	WHITE = curses.COLOR_WHITE


class RollDeck():
	def __init__(self, deck):
		self.original = []
		for _ in range(3):
			self.original.extend(deck)
		self.deck = RollDeck.shuffle(self.original)

	def draw(self):
		card = self.deck.pop()
		if len(self.deck) < len(self.original) // 3:
			self.deck = RollDeck.shuffle(self.original)
		return card

	@staticmethod
	def shuffle(cards):
		""" Return a new list of shuffled cards. """
		return random.sample(cards, len(cards))


class Board:
	def __init__(self, rows):
		self.rows = tuple(rows)
		self.height = len(self.rows)
		self.width = len(self.rows[0])

	def __getitem__(self, index):
		return self.rows[index]

	@classmethod
	def empty(cls, rows, cols):
		rows = tuple((0,) * cols for _ in range(rows))
		return cls(rows)

	def collides_with(self, piece):
		for (row, col), _ in piece:
			if row >= len(self.rows) or self.rows[row][col] != 0:
				return True
		return False

	def contains(self, piece):
		for (row, col), _ in piece:
			if col < 0 or col >= self.width or self.rows[row][col] != 0:
				return False
		return True

	def move_inbounds(self, piece):
		moved_piece = piece
		for (row, col), _ in piece:
			if col < 0:
				moved_piece = moved_piece.right
			elif col >= self.width:
				moved_piece = moved_piece.left
		return moved_piece

	def with_piece(self, piece, ch=None):
		new_board = list(self.rows)
		for (row_index, col), (r, c) in piece:
			row = new_board[row_index]
			char = ch or piece.shape[r][c]
			new_row = row[:col] + (char,) + row[col+1:]
			new_board[row_index] = tuple(new_row)
		return Board(new_board)


class Shape:
	def __init__(self, rows):
		assert len(rows) == len(rows[0]), "Shapes must have the same width and height"
		self.rows = rows

	@classmethod
	def from_string(cls, string, color):
		row_strs = (row.strip() for row in dedent(string).split('\n'))
		make_row = lambda row: [color if ch == 'X' else 0 for ch in row]
		rows = [make_row(row) for row in row_strs if row]
		return cls(rows)

	@property
	def rotated(self):
		rotated_rows = list(zip(*self.rows))[::-1]
		return Shape(rotated_rows)

	def __len__(self):
		return len(self.rows)

	def __getitem__(self, index):
		return self.rows[index]


class Piece:
	def __init__(self, prototype, origin, rotation=0):
		self.prototype = prototype
		self.rotation = rotation
		self.origin = origin
		self.shape = prototype.rotations[rotation]
		self.height = len(self.shape)
		self.width = len(self.shape[0])

	def __iter__(self):
		for r in range(self.height):
			for c in range(self.width):
				if self.shape[r][c] != 0:
					location = Pos(r + self.origin.row, c + self.origin.col)
					relative = Pos(r, c)
					yield (location, relative)

	def to_lines(self):
		result = []
		for r in range(self.height):
			line = ""
			for c in range(self.width):
				if self.prototype.shape[r][c] == 0:
					line += "  "
				else:
					line += "{0}{0}".format(self.prototype.shape[r][c])
			result += [line]
		return result


	def copy(self, rotation=None, origin=None):
		if rotation is None:
			rotation = self.rotation
		return Piece(self.prototype, origin or self.origin, rotation)

	@property
	def down(self):
		return self.copy(origin=Pos(self.origin.row + 1, self.origin.col))

	@property
	def up(self):
		return self.copy(origin=Pos(self.origin.row - 1, self.origin.col))

	@property
	def right(self):
		return self.copy(origin=Pos(self.origin.row, self.origin.col + 1))

	@property
	def left(self):
		return self.copy(origin=Pos(self.origin.row, self.origin.col - 1))

	@property
	def rotated(self):
		import time

		next_rotation = (self.rotation + 1) % len(self.prototype.rotations)
		return self.copy(rotation=next_rotation)



class ProtoPiece:
	def __init__(self, color, shape, rotations=None):
		shape = Shape.from_string(shape, color.value)

		self.shape = shape
		self.rotations = [shape]

		num_rotations = (rotations or len(shape)) - 1
		for _ in range(num_rotations):
			shape = shape.rotated
			self.rotations.append(shape)

		self.rotations = self.rotations[::-1]

	def create(self, origin=None):
		origin = origin or Pos(0, 0)
		return Piece(self, origin)



prototypes = {
	'I': ProtoPiece(Color.RED,
		"""
		.X..
		.X..
		.X..
		.X..
		""", 2),
	'J': ProtoPiece(Color.YELLOW,
		"""
		...
		XXX
		..X
		""", 4),
	'L': ProtoPiece(Color.MAGENTA,
		"""
		...
		XXX
		X..
		""", 4),
	'O': ProtoPiece(Color.BLUE,
		"""
		....
		.XX.
		.XX.
		....
		""", 1),
	'S': ProtoPiece(Color.CYAN,
		"""
		...
		.XX
		XX.
		""", 2),
	'T': ProtoPiece(Color.GREEN,
		"""
		...
		XXX
		.X.
		""", 4),
	'Z': ProtoPiece(Color.WHITE,
		"""
		...
		XX.
		.XX
		""", 2),
}


pieces = prototypes.values()







