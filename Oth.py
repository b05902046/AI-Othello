import pygame

#init screen
pygame.init()
GREEN = (0, 153, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (237, 217, 177)
screen = pygame.display.set_mode((500, 500))
screen.fill((237, 217, 177))
center = pygame.draw.rect(screen, GREEN, pygame.Rect(50, 50, 400, 400))
  #draw lines
for dist in range(50, 500, 50):
	pygame.draw.line(screen, BLACK, [dist, 50], [dist, 450])
	pygame.draw.line(screen, BLACK, [50, dist], [450, dist])

  #create index
font = pygame.font.Font(None, 30)
for num in range(0, 8):
	index = chr(ord('a') + num)
	text = font.render(str(num + 1), True, BLACK)
	screen.blit(text, (70 + num * 50,20))
	text = font.render(str(num + 1), True, BLACK)
	screen.blit(text, (20, 70 + num * 50))

done = False
turn = 1#black piece for 1, white piece for 2
  #Scoreboard
pygame.draw.circle(screen, (0,0,0), (125,475), 15)
font = pygame.font.Font(None, 45)
text = font.render('2', True, BLACK)
screen.blit(text, (165, 462))
pygame.draw.circle(screen, WHITE, (325,475), 15)
text = font.render('2', True, BLACK)
screen.blit(text, (358, 462))

  #pieces
pygame.draw.circle(screen, WHITE, (225, 225), 15)
pygame.draw.circle(screen, WHITE, (275, 275), 15)
pygame.draw.circle(screen, BLACK, (275, 225), 15)
pygame.draw.circle(screen, BLACK, (225, 275), 15)
#============board=============#

BASE = 2#position of up-left corner


#============price_table==========#
price_table = [ [0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(9) ]

#=================================#


pygame.display.flip()
def changeScore(font, black, white):#score of black
	#remove old score
	pygame.draw.rect(screen, BROWN, pygame.Rect(352, 452, 45, 45))
	pygame.draw.rect(screen, BROWN, pygame.Rect(152, 452, 45, 45))

	#set new score
	text = font.render(str(black), True, BLACK)
	if black >= 10:
		screen.blit(text, (158, 462))
	else:
		screen.blit(text, (165, 462))
	text = font.render(str(white), True, BLACK)
	if white >= 10:
		screen.blit(text, (358, 462))
	else:
		screen.blit(text, (365, 462))
	return black + white

X = [1, 1, 0, -1, -1, -1, 0, 1]
Y = [0, -1, -1, -1, 0, 1, 1, 1]
COLOR = (BROWN, BLACK, WHITE)
class gameState:
	def __init__(self, prevState = None):
		if prevState != None:
			self.board = prevState.board
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

	def changePiece_s(self, xfrom, xto, yfrom, yto, color, draw):
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
				if draw:
					pygame.draw.rect(screen, GREEN, pygame.Rect(BASE + y * 50, BASE + x * 50, 45 , 45))
					pygame.draw.circle(screen, color, (27 + y * 50, 27 + x * 50), 15)

	def changePiece_d(self, xfrom, xto, yfrom, yto, color, draw):
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
			if draw:
				pygame.draw.rect(screen, GREEN, pygame.Rect(BASE + yfrom * 50, BASE + x * 50, 45, 45))
				pygame.draw.circle(screen, color, (27 + yfrom * 50, 27 + x * 50), 15)
			yfrom += y

	def check(self, x, y, myColor, check, draw):#coordinates
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
							self.changePiece_d(x, tmpx, y, tmpy, COLOR[myColor], draw)
						else:
							self.changePiece_s(x, tmpx, y, tmpy, COLOR[myColor], draw)
					done = True
				else:
					if self.board[tmpx][tmpy] == 0:
						done = True
					else:#opponent
						add += 1
						continue
		return ret

	def get_legal_moves(self, myColor):
		moves = []
		for i in range(1, 9):
			for j in range(1, 9):
				if self.board[i][j] == 0:
					result = self.check(i, j, myColor, 1, False)
					if result > 0:
						moves += [[i, j, result]]
	        #[x, y, score]
		print "Possible moves:"
		print moves
		return moves

	def get_successor_state(self, myColor, i, j):
		successor = gameState(self)
		successor.check(i, j, myColor, 0, False)
		return successor

	def haveMove(self, myColor):
		if len(self.get_legal_moves(myColor)) > 0:
			return 1
		return -1





"""=======================================added==================================="""
def get_price_table():
	f = open("eval.txt", "r")
	temp = f.read().split()
	for i in range(1, 9):
		for j in range(1, 9):
			price_table[i][j] = int(temp[(i - 1)*8 + (j - 1)])
	f.close()

def write_price_table():
	f = open("eval.txt", "w+")
	for i in range(1, 9):
		for j in range(1, 9):
			f.write(str(price_table[i][j]) + ' ')
	f.close()

def naiive_get_best_move(currentState, myColor):
	max, maxi, maxj = -1, -1, -1
	moves = currentState.get_legal_moves(myColor)
	for [i, j, score] in moves:
		if max < score:
			max, maxi, maxj = score, i, j
	return [maxi, maxj]

def min_max_get_best_move(myColor):
	return
"""=======================================added==================================="""



if __name__ == "__main__":
	origin_board = gameState()
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		success = False
		get_price_table()
		moveable = origin_board.haveMove(turn)
		if moveable == -1:
			if turn == 1:
				turn = 2
			else:
				turn = 1
		while not success:
			if turn == 2:
				print "Computer's turn"
				#print "computer sees"
				origin_board.print_board()
				pos = naiive_get_best_move(origin_board, 2)
				print "AI chose", pos
			else:
				pos = raw_input().split()
			try:
				pos[0], pos[1] = int(pos[0]), int(pos[1])
			except:
				print "Wrong input format"
				continue
			if pos[0] > 8 or pos[0] < 1 or pos[1] > 8 or pos[1] < 1 or origin_board.occupation(pos[0], pos[1]):#position occupied or out of range
				print "illegal move"
			else:
				print "turn", turn
				result = origin_board.check(pos[0], pos[1], turn, 0, True)
				origin_board.print_board()
				if result > 0:
					white, black = origin_board.count_wb()

					total = black + white 
					changeScore(font, black, white)
					success = True
					if turn == 1:
						turn = 2
					else:
						turn = 1
					
					origin_board.print_board()

					if total == 64:
						done = True
						if black > white:
							print "Black Wins"
						elif white > black:
							print "White Wins"
						else:
							print "Draw"
				else:
					print "illegal move"

		pygame.display.flip()
"""
while not done:
	for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			changeScore(font, 3, 15)



        pygame.display.flip()

"""
