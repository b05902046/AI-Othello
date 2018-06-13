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
	moves = currentState.get_legal_moves(myColor, False)
	if warn == True:
		if len(moves) == 0:
			value = currentState.evaluate(priceTable)
			#print (depth, None, None, value)
			return (None, None, value)
	elif len(moves) == 0:
		return min_max_get_best_move(priceTable, currentState, (3-myColor), depth, True)
	if myColor == 1:
		#black
		MAX, maxi, maxj = float('-inf'), None, None
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
		MIN, mini, minj = float('inf'), None, None
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

def alpha_beta(priceTable, currentState, myColor, depth, warn, alpha, beta):
	if depth == limit_depth:
		value = currentState.evaluate(priceTable)
		return (None, None, value)
	moves = currentState.get_legal_moves(myColor, False)
	if warn == True:
		if len(moves) == 0:
			value = currentState.evaluate(priceTable)
			#print (depth, None, None, value)
			return (None, None, value)
	elif len(moves) == 0:
		return alpha_beta(priceTable, currentState, (3-myColor), depth, True, alpha, beta)
	if myColor == 1:
		#black
		MAX, maxi, maxj = float('-inf'), None, None
		for move in moves:
			newState = currentState.get_successor_state(myColor, move[0], move[1])
			new = alpha_beta(priceTable, newState, 2, depth+1, False, alpha, beta)
			if new[2] > MAX:
				MAX, maxi, maxj = new[2], move[0], move[1]
			alpha = max(MAX, alpha)
			if alpha > beta:
				break
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
			new = alpha_beta(priceTable, newState, 1, depth+1, False, alpha, beta)
			if new[2] < MIN:
				MIN, mini, minj = new[2], move[0], move[1]
			beta = min(MIN, beta)
			if alpha > beta:
				break
		#print "score", MIN
		#print "after 2"
		#currentState.print_board()
		return (mini, minj, MIN)
	
