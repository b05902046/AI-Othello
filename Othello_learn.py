import time
import method
GREEN = (0, 153, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (237, 217, 177)
BASE = 2#position of up-left corner
#=======limits=======#
limit_depth = 5
dice = 0.8
reward = 0.3
print_or_not = True

class game:
	def __init__(self):
		self.done = False
		self.turn = 1#black piece for 1, white piece for 2
#============board=============#

		self.origin_board = gameState()
#============price_table==========#
		self.price_table = [ [0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(9) ]
#=================================#

	
	def get_board(self):
		return self.origin_board

	def get_done(self):
		return self.done

	def get_turn(self):
		return self.turn

	def get_winner(self):
		return self.winner

	def get_price_table(self):
		return self.price_table

	def set_winner(self, black, white, nobody):
		self.done = True
		if black > white:
			if print_or_not == True:
				print "Black Wins"
			self.winner = 1
		elif white > black:
			if print_or_not == True:
				print "White Wins"
			self.winner = 2
		else:
			if print_or_not == True:
				print "Draw"
			self.winner = 0
		for i in range(1, 9):
			for j in range(1, 9):
				if self.origin_board.occupation(i, j) == False:
					nobody.append((i, j))

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

	def read_price_table(self):
		f = open("eval.txt", "r")
		temp = f.read().split()
		for i in range(1, 9):
			for j in range(1, 9):
				self.price_table[i][j] = float(temp[(i - 1)*8 + (j - 1)])
		f.close()

	def write_price_table(self):
		f = open("eval.txt", "w+")
		for i in range(1, 9):
			for j in range(1, 9):
				f.write(str(self.price_table[i][j]) + ' ')
			f.write('\n')
		f.close()
	
	"""
	def changeScore(self, font, black, white):#score of black
		return black + white
	"""
	def handle(self, bmoves, wmoves, nobody, learn):
		while not self.get_done():
			success = False
			self.read_price_table()
			if self.origin_board.haveMove(self.turn) == -1:
				self.next_turn()
				if self.origin_board.haveMove(self.turn) == -1:
					#game ends
					white, black = self.origin_board.count_wb()
					self.set_winner(black, white, nobody)
				#raw_input()
					success = True
					self.set_done(True)


			while not success:
				pos = None
				if learn == True:
					#============for learning================#
					pos = method.getAction(dice, self.price_table, self.origin_board, self.turn, limit_depth, "alpha_rand")
					if self.turn == 1:
						bmoves.append((pos[0], pos[1]))
					else:
						wmoves.append((pos[0], pos[1]))
				else:
					if self.get_turn() == 2:
						#useless = raw_input().split()
						if print_or_not == True:
							print "Computer's turn"
							pos = method.getAction(dice, self.price_table, self.origin_board, 2, limit_depth, "alpha_rand")
						if print_or_not == True:
							print "AI chose", pos
						#time.sleep(0.5)
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
					if print_or_not == True:
						print "turn", self.get_turn()
					result = self.origin_board.check(pos[0], pos[1], self.get_turn(), 0)
					#self.origin_board.print_board()
					if result > 0:
						white, black = self.origin_board.count_wb()

						total = black + white
						success = True
						self.next_turn()
						if print_or_not == True:
							self.origin_board.print_board()
						if total == 64:
							self.set_winner(black, white, nobody)
						
							#raw_input()

					else:
						print "illegal move"



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

	def changePiece_s(self, xfrom, xto, yfrom, yto, color):
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
				
	def changePiece_d(self, xfrom, xto, yfrom, yto, color):
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
			yfrom += y

	def check(self, x, y, myColor, check):#coordinates
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
							self.changePiece_d(x, tmpx, y, tmpy, COLOR[myColor])
						else:
							self.changePiece_s(x, tmpx, y, tmpy, COLOR[myColor])
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
	control = raw_input().split()
	if int(control[0]) == -1:
		print "play mode"
		Game = game()
		Game.handle([], [], [], False)
	else:
		black_wins, white_wins, repeat, limit_depth = 0, 0, int(control[0]), int(control[1])
		print "learn mode\nrepeat times:", repeat, "depth:", limit_depth
		print_or_not = False
		for i in range(0, repeat):
			if i%10 == 0:
				print i, "th times"
			Game = game()
			bmoves, wmoves, nobody = [], [], []
			Game.handle(bmoves, wmoves, nobody, True)
			winner = Game.get_winner()
			priTable = Game.get_price_table()
			if winner == 1:
				black_wins = black_wins + 1
				for move in bmoves:
					priTable[move[0]][move[1]] += 2*reward
				for move in nobody:
					priTable[move[0]][move[1]] += reward		
			elif winner == 2:
				white_wins = white_wins + 1
				for move in wmoves:
					priTable[move[0]][move[1]] += 2*reward
				for move in bmoves:
					priTable[move[0]][move[1]] += reward
			Game.normalize_price_table()
			Game.write_price_table()
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

