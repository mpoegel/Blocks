'''
author: Matt Poegel
date: 01/16/2014
'''

import Tkinter as tk
import random as r
import time
#CLASSES
from Window import *
from Square import *
from Field import *

colorList = ["blue", "red", "green", "yellow"]


def initialize_board():
	'''Initialize a Field object with a 100 Square objects and return the Field object'''
	board = []
	w = 30 # width of each square in pixels
	for id in range(100): #initialize 100 squares
		xp = (id%10) * w + 50 # pixels from the left edge with 50 px padding
		yp = (id/10) * w + 50 # pixels from the top edge with 50 px padding
		color = r.choice(colorList)
		box = Square(xp,yp,w,color,id)
		board.append(box)
	board = Field(board)
	return board

def on_square_click(event, board, square):
	'''Controls what will happen when specific square is clicked. If the chain length is greater
	than 1, calls upon the board to update itself.'''
	color = square.color
	id = square.id 
	row = id / 10
	col = id % 10
	chain = board.get_chain(id)
	s = len( chain )
	
	if s > 1:
		board.update(chain,app) # removes all squares in the chain from the board
		board.print_board(app, board, on_square_click)
		app.update_moves( board.move_count() ) 
		app.update_score(s)
		
def new_game(m):
	'''Starts a new game based on the requested mode number'''
	if m == 0: # new whiteout game
		board = initialize_board()
		board.print_board(app, board, on_square_click)
		
	app.score = 0
	app.time = 0
	app.moves = ''
	app.update_score(0)
	app.tick() # updates the time and checks the move count every second
	
	
#######################################
if __name__ == '__main__':
	
	root = tk.Tk()
	root.title('Blocks')
	width, height = 400,400
	mode = 0
	app = Window(root, width, height, new_game, mode, 'highscores.txt')
	
	new_game(0)
	
	
	root.mainloop()
	
	
	
	
	
	