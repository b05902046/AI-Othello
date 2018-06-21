#include "agent.hpp"


sucInform Agent::alphaBeta(const Board &board, double alpha, double beta, const int &depth, bool warn){
	sucInform ret;
	if(depth == depthLimit){
		ret.eval = evaluateBoard(board); return ret;
	}
	Board tempBoard(board); vector<Square> legalMoves = tempBoard.getLegalMoves();
	if(legalMoves.empty()){
		if(warn){
			bitset<64> black = board.getAllBlack(), white = board.getAllWhite();
			int bNum = black.count(), wNum = white.count();
			if(bNum > wNum) ret.eval = INF-1;
			else ret.eval = (bNum < wNum)? (MINF+1):(0.0);
			return ret;
		}else{
			tempBoard.reverseTurn();
			return alphaBeta(tempBoard, alpha, beta, depth, true);
		}
	}
	int n=legalMoves.size(); sucInform childInform;
	if(tempBoard.isBlacksTurn()){
		double max = MINF;
		for(int i=0;i<n;++i){
			Board nextBoard(tempBoard); nextBoard.changeBoard(legalMoves[i]);
			childInform = alphaBeta(nextBoard, alpha, beta, depth+1, false);
			if(childInform.eval > max){
				ret.eval = max = childInform.eval;
				ret.moves.clear(); ret.moves.push_back(legalMoves[i]);
			}else if(childInform.eval == max)
				ret.moves.push_back(legalMoves[i]);
			else continue;
			if(childInform.eval > alpha){
				alpha =  childInform.eval;
				if(beta < alpha) break;
			}
		}
	}else{
		double min = INF;
		for(int i=0;i<n;++i){
			Board nextBoard(tempBoard); nextBoard.changeBoard(legalMoves[i]);
			childInform = alphaBeta(nextBoard, alpha, beta, depth+1, false);
			if(childInform.eval < min){
				ret.eval = min = childInform.eval;
				ret.moves.clear(); ret.moves.push_back(legalMoves[i]);
			}else if(childInform.eval == min)
				ret.moves.push_back(legalMoves[i]);
			else continue;
			if(childInform.eval < beta){
				beta = childInform.eval;
				if(beta < alpha) break;
			}
		}
	}
	return ret;
}
