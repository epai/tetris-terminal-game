from tetris import setup
from tetris.setup import Board, RollDeck

class Game:
	def __init__(self, rows=23, cols=10):
		self.landed = Board.empty(rows, cols)
		self.deck = RollDeck(setup.pieces)
		self.next_piece = self.create_piece()
		self.curr_piece = None
		self.cleared_lines = 0
		self.has_ended = False
		self.score = 0
		self.level = 1

	def create_piece(self):
		proto_piece = self.deck.draw()
		col = 0 if proto_piece == setup.prototypes['I'] else 3
		return proto_piece.create(origin=setup.Pos(0, col))

	def new_piece(self):
		self.curr_piece = self.next_piece
		self.next_piece = self.create_piece()
		if self.landed.collides_with(self.curr_piece):
			self.has_ended = True

	def fall_piece(self):
		down_piece = self.curr_piece.down
		if self.landed.collides_with(down_piece):
			self.landed = self.landed.with_piece(self.curr_piece)
			self.clear_lines()
			return True
		self.curr_piece = down_piece
		return False

	def drop_piece(self):
		fallen = False
		while not fallen:
			fallen = self.fall_piece()

	def move_piece(self, movedir):
		if not movedir:
			return
		piece = self.curr_piece
		moved_piece = piece.left if movedir == -1 else piece.right
		if self.landed.contains(moved_piece):
			self.curr_piece = moved_piece

	def rotate_piece(self):
		rotated_piece = self.curr_piece.rotated
		moved_piece = self.landed.move_inbounds(rotated_piece)
		self.curr_piece = moved_piece

	def simulate_land(self):
		landed = False
		piece = self.curr_piece.down
		while not self.landed.collides_with(piece):
			piece = piece.down
		# get piece right before it collided
		return piece.up

	def clear_lines(self):
		score, combo = 0, 0
		for row in range(self.landed.height):
			is_filled = True
			for col in range(self.landed.width):
				if self.landed[row][col] == 0:
					is_filled = False
					break
			if is_filled:
				empty = (0,) * self.landed.width
				self.landed = Board((empty,) + self.landed.rows[:row] + self.landed.rows[row+1:])
				self.cleared_lines += 1
				score += self.landed.width * self.level * 1000 # arbitrary score calculation...
				combo += 1
		self.score += score * combo

	def __str__(self):
		piece = self.simulate_land()
		board = self.landed.with_piece(piece, 9).with_piece(self.curr_piece)
		result = ".." * (board.width + 2) + "\n"
		for r in range(1, board.height):
			result += "||"
			for c in range(board.width):
				if board[r][c] != 0:
					result += "{0}{0}".format(board[r][c])
				else:
					result += "  "
			result += "||\n"
		result += "^^" * (board.width + 2)
		return result
