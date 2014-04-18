import Tkinter as tk
import datetime


class Window(object):
	def __init__(self, parent, maxx, maxy, play_func, m, hs_file):
		'''Creates a Window object from a parent TK object containing a TK canvas
		   of dimensions maxx and maxy, menu bar, and status bars'''
		self.parent = parent
		self.mode = m
		self.hs_file = hs_file
		
		self.WO_hs = dict() # Whiteout high scores
		self.MA_hs = dict() # Marathon high scores 
		i = 0
		# open the scores files and store the data in a local dictionary
		for line in open(self.hs_file):
			line = line.strip().strip('\n')
			data = line.split()
			if len(data) == 5:
				mode = data[1]
				if mode == 'whiteout':
					self.WO_hs[i] = { 'name':data[0], 'score':data[2], 'time':data[3], 'date':data[4] }
				elif mode == 'marathon':
					pass
			i += 1
		
		## Canvas
		self.canvas = tk.Canvas(self.parent, width=maxx, height=maxy, background="white")
		self.canvas.grid(row=1, column=0, columnspan=3)
		
		## Menu Bar
		self.menubar = tk.Menu(self.parent)
		
		filemenu = tk.Menu(self.menubar, tearoff=0)
		filemenu.add_command(label="New Game", command=lambda: self.change_mode(play_func, self.mode))
		# filemenu.add_checkbutton(label='Pause', command=lambda: self.add_time == 1 if self.add_time==0 else 0)
		filemenu.add_command(label='Highscores', command=self.display_highscores)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.parent.quit)
		self.menubar.add_cascade(label="File", menu=filemenu)
		
		gmode_menu = tk.Menu(self.menubar, tearoff=0)
		gmode_menu.add_radiobutton(label='Whiteout', command=lambda: self.change_mode(play_func, 0))
		gmode_menu.add_radiobutton(label='Marathon', command=lambda: self.change_mode(play_func, 1))
		self.menubar.add_cascade(label='Game Mode', menu=gmode_menu)
		
		self.menubar.add_cascade(label='Help')
		
		self.parent.config(menu = self.menubar)
		
		## Status bars
		self.score = 0
		self.score_var = tk.StringVar()
		self.score_var.set('Score: ' + str(self.score))
		self.score_box = tk.Label(self.parent, textvariable=self.score_var)
		self.score_box.grid(row=2,column=0)
		
		self.moves = ''
		self.moves_var = tk.StringVar()
		self.moves_var.set('Moves: ' + str(self.moves))
		self.moves_box = tk.Label(self.parent, textvariable=self.moves_var)
		self.moves_box.grid(row=2,column=1)
		
		self.time = 0
		self.add_time = 1
		self.time_var = tk.StringVar()
		self.time_var.set('Time: ' +str(self.time))
		self.time_box = tk.Label(self.parent, textvariable=self.time_var)
		self.time_box.grid(row=2,column=2)
		
		self.game_mode_var = tk.StringVar()
		self.game_mode_var.set( 'Game Mode: ' + self.get_game_mode() )
		self.game_mode_box = tk.Label(self.parent, textvariable=self.game_mode_var)
		self.game_mode_box.grid(row=0,column=0,columnspan=3)
		
		
	def change_mode(self, play_func, m):
		'''Change the current game mode to m and start a new game'''
		self.mode = m
		self.game_mode_var.set( 'Game Mode: ' + self.get_game_mode() )
		play_func(m)
		
	def get_game_mode(self):
		'''Returns the game mode as a string'''
		if self.mode == 0:
			return 'Whiteout'
		elif self.mode == 1:
			return 'Marathon'
		return 'ERROR'
		
	def update_score(self, s):
		'''Adds s to the score and updates display'''
		self.score += s 
		self.score_var.set('Score: ' + str(self.score))
		
	def update_moves(self, m):
		'''Updates the display to m moves'''
		self.moves = m
		self.moves_var.set('Moves: ' + str(self.moves))
		
	def draw_rect(self, bounding_box, color, id, func, board, square):
		'''Draws a square on the canvas from a 4-tuple bounding box, a color, id number, function on click
		board reference, and square reference'''
		sq_id = self.canvas.create_rectangle(bounding_box, fill=color, tags=id)
		self.canvas.tag_bind(sq_id, '<Button-1>', lambda event: func(event, board, square))
		self.canvas.update()
		
	def clear_canvas(self):
		'''Delete all objects drawn on the canvas'''
		self.canvas.delete(tk.ALL)
		
	def tick(self):
		'''Updates the time and checks for Game Over conditions'''
		self.time += self.add_time
		self.time_var.set('Time: ' + str(self.time))
		if self.moves == 0:
			self.game_mode_var.set('GAME OVER')
			self.check_highscores()
		else:
			self.canvas.after(1000, self.tick)
			
	def check_highscores(self):
		'''Check to see if the current score is a high score for the game mode. If True, 
		get user name, calls add and save'''
		high_time = 0
		low_score = 0
		# for whiteout game mode, score must be 100, high scores are times
		if self.mode == 0 and self.score == 100:
			the_scores = self.WO_hs
			for data in the_scores.values():
				if not high_time or int(data['time']) > high_time:
					high_time = data['time']
		elif self.mode == 1: # not implemented!
			the_scores = self.MA_hs
			for data in the_scores.values():
				if not low_score or int(data['score']) < low_score:
					low_score = int(data['score'])
		else: # error
			return False

			
		if len(the_scores) < 5 or ( self.mode == 1 and self.score > low_score ) \
							   or ( self.mode == 2 and self.time < high_time ): # NEW HIGH SCORE!
			self.clear_canvas()
			self.canvas.create_text( (200,50), text='NEW HIGH SCORE!' )
			self.canvas.create_text( (200,80), text='Your Score: ' + str(self.score) )
			self.canvas.create_text( (200,95), text='Your Time: ' + str(self.time))
			self.canvas.create_text( (190,140), text='Enter Your Name:', anchor='e' )
			name = tk.StringVar()
			entry = tk.Entry(self.parent, textvariable=name)
			entry.focus()
			self.canvas.create_window( (200,140), window=entry, anchor='w' )
			submit = tk.Button( self.parent, text='Submit', padx=5, pady=5, command=lambda: self.add_highscore(the_scores, name.get(), low_score, high_time) )
			self.canvas.create_window( (200,180), window=submit )
		else: # no high score
			return False 
	
	def add_highscore(self, hs_data, name, low_score, high_time):
		'''Add the current game data to the local high score dictionary and call save'''
		hs_data[6] = { 'name':name, 'score':self.score, 'time':self.time, 'date':datetime.date.today() }
		
		# if there are more than 5 scores, delete the lowest score
		if len(hs_data) > 5:
			for k,data in hs_data.items():
				if data['time'] == high_time or data['score'] == low_score:
					del hs_data[k]
		
		self.save_highscore()
		self.canvas.create_text( (200,220), text='High Score Added!' )	
	
	def save_highscore(self):
		'''Write the local high scores data structures to the high score file'''
		save = open(self.hs_file, 'w')
		for k,data in self.WO_hs.items():
			# NAME GAMEMODE SCORE TIME DATE
			line = data['name'] + ' ' + self.get_game_mode().lower() + ' ' + str(data['score']) + ' ' + str(data['time']) + ' ' + str(data['date'])
			save.write(line + '\n')
		save.close()
	
	def display_highscores(self):
		self.moves = 0
		self.clear_canvas()
		self.canvas.create_text( (200,30), text='HIGH SCORES' )
		self.canvas.create_text( (10,45), text='Game Mode: Whiteout', anchor='w' )
		self.canvas.create_text( (20,60), text='Name', anchor='w' )
		self.canvas.create_text( (150,60), text='Score', anchor='w' )
		self.canvas.create_text( (200,60), text='Time', anchor='w' )
		self.canvas.create_text( (250,60), text='Date', anchor='w' )
		i = 0
		for val in self.WO_hs.values():
			self.canvas.create_text( (20,75+15*i), text=self.WO_hs(val['name']) )
			i += 1
		
		self.canvas.create_text( (10,45+15*7), text='Game Mode: Marathon', anchor='w' )
		
	
	
	
	
	
	
	
