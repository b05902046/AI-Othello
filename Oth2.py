import pygame
import time
GREEN = (0, 153, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (237, 217, 177)
BASE = 2#position of up-left corner
#=======limits=======#
limit_depth = 5

class game:
	def __init__(self):
#init screen
		pygame.init()
		self.screen = pygame.display.set_mode((500, 500))
		self.screen.fill((237, 217, 177))
		self.center = pygame.draw.rect(self.screen, GREEN, pygame.Rect(50, 50, 400, 400))
#draw lines
		for dist in range(50, 500, 50):
			pygame.draw.line(self.screen, BLACK, [dist, 50], [dist, 450])
			pygame.draw.line(self.screen, BLACK, [50, dist], [450, dist])

#create index
			self.font = pygame.font.Font(None, 30)
		for num in range(0, 8):
			index = chr(ord('a') + num)
			self.text = self.font.render(str(num + 1), True, BLACK)
			self.screen.blit(self.text, (70 + num * 50,20))
			self.text = self.font.render(str(num + 1), True, BLACK)
			self.screen.blit(self.text, (20, 70 + num * 50))

		self.done = False
		self.turn = 1#black piece for 1, white piece for 2
#Scoreboard
		pygame.draw.circle(self.screen, (0,0,0), (125,475), 15)
		self.font = pygame.font.Font(None, 45)
		self.text = self.font.render('2', True, BLACK)
		self.screen.blit(self.text, (165, 462))
		pygame.draw.circle(self.screen, WHITE, (325,475), 15)
		self.text = self.font.render('2', True, BLACK)
		self.screen.blit(self.text, (358, 462))
	
#pieces
		pygame.draw.circle(self.screen, WHITE, (225, 225), 15)
		pygame.draw.circle(self.screen, WHITE, (275, 275), 15)
		pygame.draw.circle(self.screen, BLACK, (275, 225), 15)
		pygame.draw.circle(self.screen, BLACK, (225, 275), 15)
#============board=============#

		self.origin_board = gameState()
#============price_table==========#
		self.price_table = [ [0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(9) ]
#=================================#
		pygame.display.flip()
	
	def get_board(self):
		return self.origin_board

	def get_done(self):
		return self.done

	def get_turn(self):
		return self.turn

	def get_winner(self, black, white):
		self.done = True
		if black > white:
			print "Black Wins"
		elif white > black:
			print "White Wins"
		else:
			print "Draw"
			
	def set_done(self, param):
		self.done = param

	def set_turn(self, param):
		self.turn = param
		
	def next_turn(self):
		if self.get_turn() == 1:
			self.set_turn(2)
		else:
			self.set_turn(1)

	def read_price_table(self):
		f = open("eval.txt", "r")
		temp = f.read().split()
		for i in range(1, 9):
			for j in range(1, 9):
				self.price_table[i][j] = int(temp[(i - 1)*8 + (j - 1)])
		f.close()

	def write_price_table(self):
		f = open("eval.txt", "w+")
		for i in range(1, 9):
			for j in range(1, 9):
				f.write(str(self.price_table[i][j]) + ' ')
		f.close()
	
	def get_price_table(self):
		return self.price_table

	def changeScore(self, font, black, white):#score of black
	#remove old score
		pygame.draw.rect(self.screen, BROWN, pygame.Rect(352, 452, 45, 45))
		pygame.draw.rect(self.screen, BROWN, pygame.Rect(152, 452, 45, 45))

	#set new score
		self.text = font.render(str(black), True, BLACK)
		if black >= 10:
			self.screen.blit(self.text, (158, 462))
		else:
			self.screen.blit(self.text, (165, 462))
		self.text = font.render(str(white), True, BLACK)
		if white >= 10:
			self.screen.blit(self.text, (358, 462))
		else:
			self.screen.blit(self.text, (365, 462))
		return black + white

	def handle(self):
		while not self.get_done():
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.set_done(True)
			success = False
			self.read_price_table()
			if self.origin_board.haveMove(self.turn) == -1:
				self.next_turn()
				if self.origin_board.haveMove(self.turn) == -1:
					#game ends
					self.get_winner(self.origin_board.count_wb())

			while not success:
				pos = None
				if self.get_turn() == 2:
					print "Computer's turn"
					#pos = naiive_get_best_move(self.origin_board, 2)
					pos = min_max_get_best_move(self.price_table, self.origin_board, 2, 1, False)
					print "AI chose", pos
					time.sleep(2)
				else:
					pos = raw_input().split()
					try:
						pos[0], pos[1] = int(pos[0]), int(pos[1])
					except:
						print "Wrong input format"
						continue
				if pos[0] > 8 or pos[0] < 1 or pos[1] > 8 or pos[1] < 1 or self.origin_board.occupation(pos[0], pos[1]):#position occupied or out of range
					print "illegal move"
				else:
					print "turn", self.get_turn()
					result = self.origin_board.check(pos[0], pos[1], self.get_turn(), 0, self.screen)
					#self.origin_board.print_board()
					if result > 0:
						white, black = self.origin_board.count_wb()

						total = black + white
						self.changeScore(self.font, black, white)
						success = True
						self.next_turn()
					
						self.origin_board.print_board()

						if total == 64:
							self.get_winner(black, white)

					else:
						print "illegal move"

			pygame.display.flip()

X = [1, 1, 0, -1, -1, -1, 0, 1]
Y = [0, -1, -1, -1, 0, 1, 1, 1]
COLOR = (BROWN, BLACK, WHITE)
class gameState:
	def __init__(self, prevBoard = None):
		if prevBoard != None:
			self.board = [ [0, 0, 0, 0, 0, 0, 0, 0, 0]  for x in range(0, 9)]
			for row in range(1,9):
				for column in range(1,9):
					self.board[row][column] = prevBoard[row][column]
			#print self.board[0] is prevBoard[0]

		else:
			self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(9)]
			self.board[4][4] = 2
			self.board[5][5] = 2
			self.board[4][5] = 1
			self.board[5][4] = 1

	def print_board(self):
		for x in self.board:
			print x
	
	def count_wb(self):
		wc, bc = 0, 0
		for i in range(1, 9):
			for j in range(1, 9):
				if(self.board[i][j] == 1):
					bc += 1
				elif(self.board[i][j] == 2):
					wc += 1
		return wc, bc

	def occupation(self, i, j):
		if self.board[i][j] > 0:
			return True
		return False

	def changePiece_s(self, xfrom, xto, yfrom, yto, color, screen = None):
		piece = 1
		if color == COLOR[2]:
			piece = 2
		if xfrom > xto:
			tmp = xfrom
			xfrom = xto
			xto = tmp
		elif yfrom > yto:
			tmp = yfrom
			yfrom = yto
			yto = tmp
		for x in range(xfrom, xto + 1):
			for y in range(yfrom, yto + 1):
				self.board[x][y] = piece
				#print "changes", x, y, "to", piece
				#self.print_board
				if screen != None:
					pygame.draw.rect(screen, GREEN, pygame.Rect(BASE + y * 50, BASE + x * 50, 45 , 45))
					pygame.draw.circle(screen, color, (27 + y * 50, 27 + x * 50), 15)

	def changePiece_d(self, xfrom, xto, yfrom, yto, color, screen = None):
		y = 1
		piece = 1
		if color == COLOR[2]:
			piece = 2
		if xfrom > xto:
			tmp = xfrom
			xfrom = xto
			xto = tmp
			if yto > yfrom:
				y = -1
			yfrom = yto
		elif yfrom > yto:
			y = -1
		for x in range(xfrom, xto + 1):
			self.board[x][yfrom] = piece
			#print "changes", x, yfrom, "to", piece
			#self.print_board
			if screen != None:
				pygame.draw.rect(screen, GREEN, pygame.Rect(BASE + yfrom * 50, BASE + x * 50, 45, 45))
				pygame.draw.circle(screen, color, (27 + yfrom * 50, 27 + x * 50), 15)
			yfrom += y

	def check(self, x, y, myColor, check, screen = None):#coordinates
		ret = 0
		for cnt in range(8):
			tmpx, tmpy, add = x, y, 0
			if tmpx + X[cnt] > 8 or tmpx + X[cnt] < 1 or tmpy + Y[cnt] > 8 or tmpy + Y[cnt] < 1 or self.board[tmpx +  X[cnt]][tmpy + Y[cnt]] == 0 or self.board[tmpx +  X[cnt]][tmpy + Y[cnt]] == myColor:
				continue
			done = False
			while not done:
				tmpx += X[cnt]
				tmpy += Y[cnt]
				if tmpx > 8 or tmpx < 1 or tmpy > 8 or tmpy < 1:
					break
				if self.board[tmpx][tmpy] == myColor:
					ret += add
					if check == 0:
						if cnt == 1 or cnt == 3 or cnt == 5 or cnt == 7:
							self.changePiece_d(x, tmpx, y, tmpy, COLOR[myColor], screen)
						else:
							self.changePiece_s(x, tmpx, y, tmpy, COLOR[myColor], screen)
					done = True
				else:
					if self.board[tmpx][tmpy] == 0:
						done = True
					else:#opponent
						add += 1
						continue
		return ret

	def get_legal_moves(self, myColor, flag):
		moves = []
		for i in range(1, 9):
			for j in range(1, 9):
				if self.board[i][j] == 0:
					result = self.check(i, j, myColor, 1)
					if result > 0:
						moves += [[i, j, result]]
	        #[x, y, score]
		if flag == True:
			print "Possible moves:"
			print moves
		return moves

	def get_successor_state(self, myColor, i, j):
		successor = gameState(self.board)
		successor.check(i, j, myColor, 0)
		return successor

	def haveMove(self, myColor):
		if len(self.get_legal_moves(myColor, True)) > 0:
			return 1
		return -1
	def evaluate(self, priceTable):
		value = 0
		for i in range(1, 9):
			for j in range(1, 9):
				if self.board[i][j] == 1:
					value += priceTable[i][j]
				elif self.board[i][j] == 2:
					value -= priceTable[i][j]
		return value

def naiive_get_best_move(currentState, myColor):
	max, maxi, maxj = -1, -1, -1
	moves = currentState.get_legal_moves(myColor, True)
	for [i, j, score] in moves:
		if max < score:
			max, maxi, maxj = score, i, j
	return [maxi, maxj]

def min_max_get_best_move(priceTable, currentState, myColor, depth, warn):
	#print "depth", depth, "myColor", myColor
	#currentState.print_board()
	if depth == limit_depth:
		value = currentState.evaluate(priceTable)
		#print (depth, None, None, value)
		return (None, None, value)
	moves = currentState.get_legal_moves(myColor, True)
	if warn == True:
		if moves == None:
			value = currentState.evaluate(priceTable)
			#print (depth, None, None, value)
			return (None, None, value)
	elif moves == None:
		return min_max_get_best_move(priceTable, currentState, (3-myColor), depth, True)
	if myColor == 1:
		#black
		MAX, maxi, maxj = -10000000000, None, None
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			new = min_max_get_best_move(priceTable, newState, 2, depth+1, False)
			if new[2] > MAX:
				MAX, maxi, maxj = new[2], move[0], move[1]
		#print "score", MAX
		#print "after"
		#currentState.print_board()
		return (maxi, maxj, MAX)
	elif myColor == 2:
		#white
		MIN, mini, minj = 10000000000, None, None
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			#print "new"
			#currentState.print_board()
			new = min_max_get_best_move(priceTable, newState, 1, depth+1, False)
			if new[2] < MIN:
				MIN, mini, minj = new[2], move[0], move[1]
		#print "score", MIN
		#print "after 2"
		#currentState.print_board()
		return (mini, minj, MIN)

"""=======================================added==================================="""



if __name__ == "__main__":
	Game = game()
	Game.handle()

"""
while not done:
	for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			changeScore(font, 3, 15)



        pygame.display.flip()

"""
