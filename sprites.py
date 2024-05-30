# sprites

from settings import *
import pygame  

class Block:
	def __init__(self, row, col, color):
		self.win = pygame.display.get_surface()
		self.row_pos = row 
		self.col_pos = col
		
		self.start_x = START_X + col * BLOCK_SIZE
		self.start_y = START_Y + row * BLOCK_SIZE
		self.x =  self.start_x
		self.y = self.start_y
		self.color = color

		self.left = False
		self.right = False
		self.up = False
		self.down = False

		self.direction = [self.left, self.right, self.up, self.down]

		self.width, self.height = 0, 0
		self.filled = False 

	def draw_block(self):
		pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

	def fill_lines_after_filled(self, blocks, color, lines):
		row, col = self.row_pos, self.col_pos
		if not lines['vertical'][(row, col)].clicked:
			lines['vertical'][(row, col)].get_clicked(blocks, (row, col))
		if not lines['vertical'][(row, col + 1)].clicked:
			lines['vertical'][(row, col + 1)].get_clicked(blocks, (row, col + 1))

		if not lines['horizontal'][(row, col)].clicked:
			lines['horizontal'][(row, col)].get_clicked(blocks, (row, col))
		if not lines['horizontal'][(row + 1, col)].clicked:
			lines['horizontal'][(row + 1, col)].get_clicked(blocks, (row + 1, col))
	
	def change_color(self, color):
		if color == "blue":
			self.color = BLUE

		elif color == "red":
			self.color = RED

	def fill_block(self, blocks, color, lines):
		self.filled = True 
		self.change_color(color)

		self.fill_lines_after_filled(blocks, color, lines)

	def check_filled(self):
		self.direction = [self.left, self.right, self.up, self.down]
		return all(self.direction)


	def update_color(self):
		if self.filled and self.width != BLOCK_SIZE:
			self.width += 2
			self.height += 2

			self.x = self.start_x + (BLOCK_SIZE // 2 - self.width // 2)
			self.y = self.start_y + (BLOCK_SIZE // 2 - self.height // 2) 
			return True
		return False

class Line:
	def __init__(self, x ,y, width, height, row, col, color, direction):
		self.win = pygame.display.get_surface()
		self.x = x 
		self.y = y 
		self.width = width 
		self.height = height 
		self.row = row 
		self.col = col
		self.color = color 
		self.direction = direction
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.clicked = False 

	def draw(self):
		pygame.draw.rect(self.win, self.color, self.rect)


	def get_clicked(self, blocks, pos):
		self.clicked = True 	
		self.color = "black"


		row, col = pos
		if self.direction == "vertical":
			if col == 0:
				blocks[row][0].left = True 

			elif col == COLS:
				blocks[row][col - 1].right = True 

			else:
				blocks[row][col].left = True
				blocks[row][col - 1].right = True


		elif self.direction == "horizontal":
			if row == 0:
				blocks[0][col].up = True 
			elif row == ROWS:
				blocks[row - 1][col].down = True 
			else:
				blocks[row][col].up = True
				blocks[row - 1][col].down = True				
