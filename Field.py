import Tkinter as tk


class Field(object):
	def __init__(self, bb):
		self.boxes = bb
		
	def get_square(self, id):
		return self.boxes[id]
		
	def move_square_down(self, id):
		if id < 90:
			self.boxes[id].move_down()
			self.boxes[id+10] = self.boxes[id]
			self.boxes[id] = None
	
	def move_square_right(self, id):
		if id%10 < 9:
			self.boxes[id].move_right()
			self.boxes[id+1] = self.boxes[id]
			self.boxes[id] = None
		
	def remove_square(self, id):
		self.boxes[id] = None
		
	def move_column_right(self, col):
		for i in range(90+col, -1, -10):
			if not self.get_square(i):
				break
			self.move_square_right(i)
			
	def slide_right(self, col):
		for i in range(col-1, -1, -1):
			self.move_column_right(i)
		
	def update(self, chain, app):
		# slide down
		for b in chain:
			id = b.id 
			self.remove_square(id)
			for i in range( id-10, (id%10)-10, -10):
				if self.get_square(i):
					self.move_square_down(i)
				else:
					break
		# slide right
		i = 98
		while i >= 90:
			if not self.get_square(i):
				self.slide_right( i%10 )
			i -= 1
	
	def move_count(self):
		count = 0
		box_copy = self.boxes[:]
		for i in range(100):
			if box_copy[i]:
				b = self.get_square(i)
				x = self.get_chain(i)
				if b and len(x) > 1:
					count += 1 
				for k in x:
					box_copy[ k.id ] = None
		return count
		
	def print_board(self, app, board, click):
		app.clear_canvas()
		for box in self.boxes:
			if box == None: continue
			app.draw_rect( box.bounding_box(), box.color, box.id, click, board, box )
			
	def look_up(self, id):
		if id%10 > 0:
			return self.get_square(id-1)
		return None
	def look_down(self, id):
		if id%10 < 9:
			return self.get_square(id+1)
		return None
	def look_right(self, id):
		if id < 90:
			return self.get_square(id+10)
		return None
	def look_left(self, id):
		if id > 10:
			return self.get_square(id-10)
		return None
			
	def matching_dir(self, id):
		color = self.get_square(id).color
		all = [self.look_left(id),
				 self.look_right(id),
				 self.look_up(id),
				 self.look_down(id),]
		match = []
		for b in all:
			if b and b.color == color:
				match.append(b)
		return match
	
	def get_chain(self, id):
		box = self.boxes[id]
		color = box.color
		matched_queue = [box]
		all_matched = set()
		all_matched.add(box)
		while len(matched_queue):
			box = matched_queue.pop(0)
			id = box.id
			matches = self.matching_dir(id)
			for m in matches:
				if not m in all_matched:
					matched_queue.append(m)
					all_matched.add(m)
		return all_matched
		
		
		
		