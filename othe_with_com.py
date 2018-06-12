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
	text = font.render(index, True, BLACK)
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
board = [ [0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(9) ]
board[4][4] = 2
board[5][5] = 2
board[4][5] = 1
board[5][4] = 1


#============price_table==========#
price_table = [ [0, 0, 0, 0, 0, 0, 0, 0, 0] for x in range(9) ]

#=================================#


pygame.display.flip()
def changeScore(font, black, white):#score of black
	black , white = 0, 0
	for row in board:
		for column in row:
			if column == 1:
				black += 1
			elif column == 2:
				white += 1
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

def changePiece_s(xfrom, xto, yfrom, yto, color):
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
			board[x][y] = piece
			pygame.draw.rect(screen, GREEN, pygame.Rect(BASE + y * 50, BASE + x * 50, 45 , 45))
			pygame.draw.circle(screen, color, (27 + y * 50, 27 + x * 50), 15)
def changePiece_d(xfrom, xto, yfrom, yto, color):
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
		board[x][yfrom] = piece
		pygame.draw.rect(screen, GREEN, pygame.Rect(BASE + yfrom * 50, BASE + x * 50, 45, 45))
		pygame.draw.circle(screen, color, (27 + yfrom * 50, 27 + x * 50), 15)
		yfrom += y
X = [1, 1, 0, -1, -1, -1, 0, 1]
Y = [0, -1, -1, -1, 0, 1, 1, 1]
COLOR = (BROWN, BLACK, WHITE)
def check(x, y, myColor, check):#coordinates
	ret = 0 
	for cnt in range(8):
		tmpx, tmpy, add = x, y, 0
		if tmpx + X[cnt] > 8 or tmpx + X[cnt] < 1 or tmpy + Y[cnt] > 8 or tmpy + Y[cnt] < 1 or board[tmpx +  X[cnt]][tmpy + Y[cnt]] == 0 or board[tmpx +  X[cnt]][tmpy + Y[cnt]] == myColor:
			continue
		done = False
		while not done:
			tmpx += X[cnt]
			tmpy += Y[cnt]
			if tmpx > 8 or tmpx < 1 or tmpy > 8 or tmpy < 1:
				break
			if board[tmpx][tmpy] == myColor:
				ret += add
				if check == 0:
					if cnt == 1 or cnt == 3 or cnt == 5 or cnt == 7:
						changePiece_d(x, tmpx, y, tmpy, COLOR[myColor])
					else:
						changePiece_s(x, tmpx, y, tmpy, COLOR[myColor])
				done = True
			else:
				if board[tmpx][tmpy] == 0:
					done = True
				else:#opponent
					add += 1
					continue
	return ret
def haveMove(myColor):
	for row in range(1, 9):
		for column in range(1, 9):
			if board[row][column] == 0:
				result = check(row, column, myColor, 1) 
				if result > 0:
					return 1
	return -1





"""=======================================added==================================="""
def get_price_table():
	f = open("eval.txt", "r")
	temp = f.read().split()
	for i in range(1, 9):
		for j in range(1, 9):
			price_table[i][j] = int(temp[i*8+j])
	f.close()

def write_price_table():
	f = open("eval.txt", "w+")
	for i in range(1, 9):
		for j in range(1, 9):
			f.write(str(price_table[i][j]) + ' ')
	f.close()

def naiive_get_best_move(myColor):
	max , maxi, maxj = -1, -1, -1
	for i in range(1, 9):
		for j in range(1, 9):
			if board[i][j] == 0:
				result = check(i, j, myColor, 1)
				if max < result:
					max, maxi, maxj = result, i, j
	return [maxi, maxj]

def min_max_get_best_move(myColor):
	return
"""=======================================added==================================="""




while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	success = False
	get_price_table()
	moveable = haveMove(turn)
	if moveable == -1:
		if turn == 1:
			turn = 2
		else:
			turn = 1
	while not success:
		if turn == 2:
			print "Computer's turn"
			pos = naiive_get_best_move(2)
		else:
			pos = raw_input().split()
		try:
			pos[0], pos[1] = int(pos[0]), int(pos[1])
		except:
			print "Wrong input format"
			continue
		if pos[0] > 8 or pos[0] < 1 or pos[1] > 8 or pos[1] < 1 or board[pos[0]][pos[1]] != 0:#position occupied or out of range
			print "illegal move"
		else:
			print "turn", turn
			result = check(pos[0], pos[1], turn, 0)
			if result > 0:
				black, white = 0, 0
				for row in board:
					for column in row:
						if column == 1:
							black += 1
						elif column == 2:
							white += 1
				total = black + white 
				changeScore(font, black, white)
				success = True
				if turn == 1:
					turn = 2
				else:
					turn = 1
				for x in board:
					print x
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
