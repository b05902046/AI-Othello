import random
def naiive_get_best_move(currentState, myColor):
	max, maxi, maxj = -1, -1, -1
	moves = currentState.get_legal_moves(myColor, True)
	for [i, j, score] in moves:
		if max < score:
			max, maxi, maxj = score, i, j
	return [maxi, maxj]

def min_max_get_best_move(priceTable, currentState, myColor, depth, limit_depth, warn):
	#print "depth", depth, "myColor", myColor
	#currentState.print_board()
	if depth == limit_depth:
		value = currentState.evaluate(priceTable)
		#print (depth, None, None, value)
		return (None, None, value)
	moves = currentState.get_legal_moves(myColor, False)
	if warn == True:
		if len(moves) == 0:
			nums = currentState.count_wb()
			if nums[1] > nums[0]:
				value = 810000
			elif nums[1] < nums[0]:
				value = -810000
			else:
				value = 0
			#print (depth, None, None, value)
			return (None, None, value)
	elif len(moves) == 0:
		return min_max_get_best_move(priceTable, currentState, (3-myColor), depth, limit_depth, True)
	if myColor == 1:
		#black
		MAX, maxi, maxj = float('-inf'), None, None
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			new = min_max_get_best_move(priceTable, newState, 2, depth+1, limit_depth, False)
			if new[2] > MAX:
				MAX, maxi, maxj = new[2], move[0], move[1]
		#print "score", MAX
		#print "after"
		#currentState.print_board()
		return (maxi, maxj, MAX)
	elif myColor == 2:
		#white
		MIN, mini, minj = float('inf'), None, None
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			#print "new"
			#currentState.print_board()
			new = min_max_get_best_move(priceTable, newState, 1, depth+1, limit_depth, False)
			if new[2] < MIN:
				MIN, mini, minj = new[2], move[0], move[1]
		#print "score", MIN
		#print "after 2"
		#currentState.print_board()
		return (mini, minj, MIN)

def alpha_beta(priceTable, currentState, myColor, depth, limit_depth, warn, alpha, beta):
	if depth == limit_depth:
		value = currentState.evaluate(priceTable)
		return [(None, None, value)]
	moves = currentState.get_legal_moves(myColor, False)
	if warn == True:
		if len(moves) == 0:
			nums = currentState.count_wb()
			if nums[1] > nums[0]:
				value = 810000.0        #something big, but smaller than float('inf')
			elif nums[1] < nums[0]:
				value = -810000.0       #something small, but bigger than float('-inf')
			else:
				value = 0
			#print (depth, None, None, value)
			return [(None, None, value)]
	elif len(moves) == 0:
		return alpha_beta(priceTable, currentState, (3-myColor), depth, limit_depth, True, alpha, beta)
	if myColor == 1:
		#black
		MAX, ret = float('-inf'), []
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			new = alpha_beta(priceTable, newState, 2, depth+1, limit_depth, False, alpha, beta)
			value = new[0][2]
			if value > MAX:
				MAX, ret = value, [(move[0], move[1], value)]
			elif value == MAX:
				ret.append((move[0], move[1], value))
			alpha = max(MAX, alpha)
			if alpha > beta:
				break
		#print "score", MAX
		#print "after"
		#currentState.print_board()
		return ret
	elif myColor == 2:
		#white
		MIN, ret = float('inf'), []
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			#print "new"
			#currentState.print_board()
			new = alpha_beta(priceTable, newState, 1, depth+1, limit_depth, False, alpha, beta)
			value = new[0][2]
			if value < MIN:
				MIN, ret = value, [(move[0], move[1], value)]
			elif value == MIN:
				ret.append((move[0], move[1], value))
			beta = min(MIN, beta)
			if alpha > beta:
				break
		#print "score", MIN
		#print "after 2"
		#currentState.print_board()
		return ret

def getAction(dice, price_table, gameState, myColor, depth_limit, method):
	moves = gameState.get_legal_moves(myColor, False)
	if method == "naiive":
		return naiive_get_best_move(gameState, myColor)
	elif method == "minimax":
		return min_max_get_best_move(price_table, gameState, myColor, 1, depth_limit, False)
	elif method == "alpha":
		alpha_beta(price_table, gameState, myColor, 1, depth_limit, False, float('-inf'), float('inf'))
		who = random.randint(0, len(moves)-1)
		return (moves[who][0], moves[who][1])		
	elif method == "alpha_rand":
		bestMove = alpha_beta(price_table, gameState, myColor, 1, depth_limit, False, float('-inf'), float('inf'))
		if random.random() <= dice:
			return (bestMove[0], bestMove[1])
		else:
			who = random.randint(0, len(moves)-1)
			return (moves[who][0], moves[who][1])
