import pygame 
from settings import * 
from sprites import Block, Line
import random

pygame.init()

# determine what block are related to the line you clicked
def block_clicked(line):
	row, col = line.row, line.col 
	block_clicked = []
	if line.direction == "vertical":
		
		if col == 0:
			block_clicked.append((row, 0))
		elif col == COLS:
			block_clicked.append((row, col - 1))
		else:
			block_clicked.append((row, col))
			block_clicked.append((row, col - 1))


	elif line.direction == "horizontal":

		if row == 0:
			block_clicked.append((0, col))
		elif row == ROWS:
			block_clicked.append((row - 1, col))
		else:
			block_clicked.append((row - 1, col))
			block_clicked.append((row, col))

	return block_clicked


# check if three or four of the block are filled
def check_three_sides(block):
	count = 0 
	if block.left:
		count += 1
	if block.right:
		count += 1 
	if block.up:
		count += 1 
	if block.down:
		count += 1 


	return count >= 3


# get left, right, up, down block of the original block
def get_neighbor(pos):
	row, col = pos 
	neighbors = []

	if row >= 0 and row < ROWS - 1:
		neighbors.append((row + 1, col))

	if row <= ROWS - 1 and row > 0:
		neighbors.append((row - 1, col))

	if col >= 0 and col < COLS - 1:
		neighbors.append((row, col + 1))

	if col <= COLS - 1 and col > 0:
		neighbors.append((row, col - 1))

	return neighbors

def generate_blocks():
	blocks = []

	for row in range(ROWS):
		in_row = []
		for col in range(COLS):
			block = Block(row, col, YELLOW)

			in_row.append(block)

		blocks.append(in_row)

	return blocks

def generate_lines():
	# direction first then position
	lines = {"vertical": dict(), "horizontal": dict()}

	for row in range(ROWS + 1):
		y = START_Y + row * BLOCK_SIZE

		for col in range(COLS + 1):
			x = START_X + col * BLOCK_SIZE

			if col == COLS:
				if row < ROWS:
					line = Line(x - LINE_SMALL // 2, y, LINE_SMALL, LINE_BIG, row, col, "white", "vertical")
					lines["vertical"][(row, col)] = line

			elif row == ROWS:
				line = Line(x, y - LINE_SMALL // 2, LINE_BIG, LINE_SMALL, row, col, "white", "horizontal")
				lines["horizontal"][(row, col)] = line

			else:
				line = Line(x - LINE_SMALL // 2, y, LINE_SMALL, LINE_BIG, row, col, "white", "vertical")
				lines['vertical'][(row, col)] = line
	
				line = Line(x, y - LINE_SMALL // 2, LINE_BIG, LINE_SMALL, row, col, "white", "horizontal")
				lines['horizontal'][(row, col)] = line

	return lines 

class Game:
	def __init__(self):
		self.win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.blocks = generate_blocks()
		self.lines = generate_lines()
		self.player = random.choice(["red", "blue"])
		self.filled_block = set()

		self.points = {"red": 0, "blue": 0}
		self.updating_block = []
		self.winner = ""

	# check if any block that filled in three sides 
	# then filled that automically 
	def check_neighbor_filled(self, pos, color):
		visited = self.filled_block
		stack = [pos]

		while stack:
			y, x = stack.pop()
			neighbors = get_neighbor((y, x))

			for row, col in neighbors:
				if (row, col) not in visited:
					if self.blocks[row][col].filled:
						visited.add((row, col))
						if (row, col) not in self.filled_block:
							self.filled_block.add((row, col))
						continue


					block = self.blocks[row][col]
					if check_three_sides(block):
						block.left = True 
						block.right = True
						block.up = True
						block.down = True

						block.fill_block(self.blocks, color, self.lines)
						self.points[self.player] += 1 

						self.filled_block.add((row, col))
						stack.append((row, col))
						visited.add((row, col))

						self.updating_block.append(block)

	def check_block_after_clicked(self, block):	
		if not block.filled:
			if block.check_filled():
				self.filled_block.add((block.row_pos, block.col_pos))
				
				# block.filled = True
				block.fill_block(self.blocks, self.player, self.lines)
				
				self.points[self.player] += 1
				self.updating_block.append(block)
				self.check_neighbor_filled((block.row_pos, block.col_pos), self.player)

				return False 

		return True

	def update_player(self):
		if self.player == "red":
			self.player = "blue"
		else:
			self.player = "red" 


	def draw_window(self):
		self.win.fill(YELLOW)

		# draw the block
		for row in self.blocks:
			for block in row:
				if block.filled == True:
					block.draw_block()


		# draw the line 
		for direction in self.lines:
			for pos in self.lines[direction]:
				self.lines[direction][pos].draw()


		# draw the circle dots 
		for row in range(ROWS + 1):
			y = START_Y + row * BLOCK_SIZE

			for col in range(COLS + 1):
				x = START_X + col * BLOCK_SIZE
					
				pygame.draw.circle(self.win, "black", (x, y), LINE_SMALL)


		# draw the player 
		if self.player == "red":
			pygame.draw.rect(self.win, RED, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 30)
		elif self.player == "blue":
			pygame.draw.rect(self.win, BLUE, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 30)


		# display point 
		font = pygame.font.SysFont("comicsans", 30)

		text1 = font.render(f"Red: {self.points['red']}", "red", False)
		self.win.blit(text1, (0, 0))

		text2 = font.render(f"Blue: {self.points['blue']}", "blue", False)
		self.win.blit(text2, (0, WINDOW_HEIGHT - text2.get_height()))

		
	def check_winner(self):
		if self.updating_block:
			return

		if not self.winner:
			for row in self.blocks:
				for block in row:
					if not block.filled:
						return 

		if self.points["red"] > self.points["blue"]:
			self.winner = "red"
		elif self.points["blue"] > self.points["red"]:
			self.winner = "blue"
		else:
			self.winner = "draw" 

	def display_winner(self):
		if self.winner:
			font = pygame.font.SysFont("comicsans", 150)

			if self.winner != "draw":
				if self.winner == "red":
					self.win.fill(RED)
				elif self.winner == "blue":
					self.win.fill(BLUE)

				text = font.render(f"{self.winner} won", False, "white")
				self.win.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2,
							WINDOW_HEIGHT // 2 - text.get_height() // 2))
			
			else:
				self.win.fill(YELLOW)

				text = font.render(f"Draw", False, "white")
				self.win.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2,
							WINDOW_HEIGHT // 2 - text.get_height() // 2))

			pygame.display.update()
			pygame.time.wait(2000)

			return True 
		return False

	def check_valid_clicked(self, x, y):
		if START_X - 5 <= x <= WINDOW_WIDTH - START_X + 5 and START_Y - 5 < y < WINDOW_HEIGHT- START_Y + 5 and not self.updating_block:
			for direction in self.lines:
				for pos in self.lines[direction]:
					line = self.lines[direction][pos]

					if line.rect.collidepoint((x, y)) and line.clicked == False:
						return line 
		return False

	def update_block_color(self):
		if self.updating_block:
			if len(self.updating_block) == 1:
				block = self.updating_block[0]

				block.update_color()

				if block.width == BLOCK_SIZE:
					self.updating_block.pop(0)

			elif len(self.updating_block) >= 2:
				block = self.updating_block[0]
				block2 = self.updating_block[1]

				block.update_color()
				block2.update_color()

				if block.width == BLOCK_SIZE:
					self.updating_block.pop(0)
					self.updating_block.pop(0)

	def resetGame(self):
		self.blocks = generate_blocks()
		self.lines = generate_lines()

		self.player = random.choice(["red", "blue"])
		self.filled_block = set()

		self.points = {"red": 0, "blue": 0}
		self.updating_block = []
		self.winner = ""

	def run(self):
		run = True 

		while run:
			change_player = True
			clicked = False

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False 
					break

				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					line = self.check_valid_clicked(x, y)
					if line:
						clicked = True
						line.get_clicked(self.blocks, (line.row, line.col))
						
						for row, col in block_clicked(line):
							block = self.blocks[row][col]
							check = self.check_block_after_clicked(block)
							if check == False:
								change_player = False
	
			self.update_block_color()

			self.draw_window()
			self.check_winner()
			reset = self.display_winner()
			
			pygame.display.update()
			if reset:
				self.resetGame()

			if change_player and clicked:
				self.update_player()

		pygame.quit()
		quit()


game = Game()
game.run()