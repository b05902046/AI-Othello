import time
import pygame
import method
GREEN = (0, 153, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (237, 217, 177)
BASE = 2#position of up-left corner
#=======limits=======#
limit_depth = 5
dice = 0.8
reward = 0.7
print_or_not = False

class game:
	def __init__(self, pTable_B, pTable_W, graph = True):
		self.screen = None
		self.winner = 0
		self.done = False
		self.turn = 1#black piece for 1, white piece for 2
		if graph == True:
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
				
			pygame.display.flip()
#============board=============#

		self.origin_board = gameState()
#============price_table==========#
		self.price_table_B = self.read_price_table(pTable_B)
		self.price_table_W = self.read_price_table(pTable_W)
#=================================#

	
	def get_board(self):
		return self.origin_board

	def get_done(self):
		return self.done

	def get_turn(self):
		return self.turn

	def get_winner(self):
		return self.winner

	def get_price_table(self, which):
		if which == 1:
			return self.price_table_B
		else:
			return self.price_table_W

	def set_winner(self, black, white):
		self.done = True
		if black > white:
			#if print_or_not == True:
			print "Black Wins"
			self.winner = 1
		elif white > black:
			#if print_or_not == True:
			print "White Wins"
			self.winner = 2
		else:
			#if print_or_not == True:
			print "Draw"
			self.winner = 0

	def set_done(self, param):
		self.done = param

	def set_turn(self, param):
		self.turn = param
		
	def next_turn(self):
		if self.get_turn() == 1:
			self.set_turn(2)
		else:
			self.set_turn(1)

	def normalize_price_table(self):
		summ = 0
		for i in range(1, 9):
			summ += sum(self.price_table[i])
		summ /= 64
		for i in range(1, 9):
			for j in range(1, 9):
				self.price_table[i][j] /= summ

	def read_price_table(self, path):
		f = open(path, "r")
		price_table = [ [0, 0, 0, 0, 0, 0, 0, 0, 0] for row in range(0, 9)]
		temp = f.read().split()
		for i in range(1, 9):
			for j in range(1, 9):
				price_table[i][j] = float(temp[(i - 1)*8 + (j - 1)])
		f.close()
		return price_table

	def write_price_table(self, price_table):
		f = open(path, "w+")
		for i in range(1, 9):
			for j in range(1, 9):
				f.write(str(self.price_table[i][j]) + ' ')
			f.write('\n')
		f.close()
	
	
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
			if graph == True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.set_done(True)
			success = False
			if self.origin_board.haveMove(self.turn) == -1:
				self.next_turn()
				if self.origin_board.haveMove(self.turn) == -1:
					#game ends
					white, black = self.origin_board.count_wb()
					if graph == True:
						pygame.display.flip()
					self.set_winner(black, white)
					success = True
					self.set_done(True)


			while not success:
				pos = None
					#============for learning================#
				if self.turn == 1:
					pos = method.getAction(dice, self.price_table_B, self.origin_board, self.turn, limit_depth, "alpha")
				else:
					pos = method.getAction(dice, self.price_table_W, self.origin_board, self.turn, limit_depth, "alpha")
				#time.sleep(0.5)

				if pos[0] > 8 or pos[0] < 1 or pos[1] > 8 or pos[1] < 1 or self.origin_board.occupation(pos[0], pos[1]):#position occupied or out of range
					print "illegal move"
				else:
					if print_or_not == True:
						print "turn", self.get_turn()
					result = self.origin_board.check(pos[0], pos[1], self.get_turn(), 0, self.screen)
					#self.origin_board.print_board()
					if result > 0:
						white, black = self.origin_board.count_wb()
						total = black + white
						if graph == True:
							self.changeScore(self.font, black, white)
						success = True
						self.next_turn()
						if print_or_not == True:
							self.origin_board.print_board()
						if total == 64:
							self.set_winner(black, white)
							if graph == True:
								pygame.display.flip()
							#raw_input()

					else:
						print "illegal move"
			if graph == True:
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
				#print_board
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
			#print_board
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
		if print_or_not == True and flag == True:
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


"""=======================================added==================================="""



if __name__ == "__main__":
	control = raw_input("repeat, depth, black table, white table2\n").split()
	black_wins, white_wins = 0, 0
	repeat, limit_depth, table_B, table_W = int(control[0]), int(control[1]), control[2], control[3]
	graph = True
	if control[4] == "n":
		graph = False
	for i in range(0, repeat):
		if i%10 == 0:
			print i, "th times"
		Game = game(table_B, table_W, graph)
		Game.handle()
		winner = Game.get_winner()
		if winner == 1:
			black_wins += 1
		elif winner == 2:
			white_wins += 1
	print "black:", black_wins, "white:", white_wins, "ties:", (repeat - black_wins - white_wins)
"""
while not done:
	for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			changeScore(font, 3, 15)



        pygame.display.flip()

"""

