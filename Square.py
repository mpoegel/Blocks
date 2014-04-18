import Tkinter as tk


class Square(object):
	def __init__(self,x0,y0,w0,c,id0):
		'''Initialize a Square object with (x,y) position (upper left corner), width, color, and ID number'''
		self.x_pos = x0
		self.y_pos = y0
		self.width = w0
		self.color = c
		self.id = id0
		
	def bounding_box(self):
		'''Returns a bounding box for the square object'''
		return (self.x_pos, self.y_pos, self.x_pos + self.width, self.y_pos + self.width)
		
	def set_id(self, new):
		'''Sets a new ID and updates the x and y positions accordingly'''
		self.id = new
		self.x_pos = new%10 * self.width
		self.y_pos = new/10 * self.width
		
	def move_down(self):
		'''Move the square down and change the id'''
		self.id += 10
		self.y_pos += 30
		
	def move_right(self):
		'''Move the square right and change the id'''
		self.id += 1
		self.x_pos += 30
	