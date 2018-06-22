#include "board.hpp"

const Square iterateOrder[60] =
#ifdef NA_ORDER
	{S11 , S12, S13, S14, S15, S16, S17, S18,
	S21, S22, S23, S24, S25, S26, S27, S28,
	S31, S32, S33, S34, S35, S36, S37, S38,
	S41, S42, S43,/* S44, S45,*/ S46, S47, S48,
	S51, S52, S53,/* S54, S55,*/ S56, S57, S58,
	S61, S62, S63, S64, S65, S66, S67, S68,
	S71, S72, S73, S74, S75, S76, S77, S78,
	S81, S82, S83, S84, S85, S86, S87, S88};
#else
	{S11, S18, S81, S88,//corners
	S13, S16, S31, S33, S36, S38, S61, S63, S66, S68, S83, S86,//possible good squares
	S14, S15, S41, S48, S51, S58, S84, S85,//edges
	S23, S24, S25, S26, S32, S34, S35, S37, S42, S43, S46, S47, S52, S53, S56, S57, S62, S64, S65, S67, S73, S74, S75, S76,//normal squares
	S12, S17, S21, S22, S27, S28, S71, S72, S77, S78, S82, S87};//possible bad squares
#endif

int Board::isWho(Square square)const{
	return (occupied[square])? ((white[square])? 2: 1) : 0;
}

Board::Board(){
	ended = false; blacksTurn = true;
	occupied.reset(); white.reset();
	setWhite(S44); setWhite(S55);
	setBlack(S45); setBlack(S54);
}

Board::Board(const Board &another){
	*this = another;
}

void Board::setGameEnded(){
	ended = true;
}

void Board::reverseTurn(){
	blacksTurn = !blacksTurn;
}

bool Board::isGameEnded()const{
	return ended;
}

int Board::whoWon(int &bn, int &wn)const{
	if(!isGameEnded()){ printf("Call whoWon when game not ended!\n"); fflush(stdout); exit(1);}
	bitset<64> black = getAllBlack(), white = getAllWhite();
	bn = black.count(); wn = white.count();
	if(bn > wn) return 1;
	else return (bn == wn)? 0:-1;
}

bool Board::isBlacksTurn()const{
	return blacksTurn;
}

bool Board::isBlack(Square square)const{
	return (occupied[square] && !white[square]);
}

bool Board::isWhite(Square square)const{
	return (occupied[square] && white[square]);
}

bool Board::isEmpty(Square square)const{
	return !occupied[square];
}

void Board::getBoardString(char *string)const{
	for(int i=0;i<64;++i)
		string[i] = '0'+isWho((Square)i);
}

bitset<64> Board::getAllEmpty()const{
	bitset<64> temp = occupied; temp.flip();
	return temp;
}

bitset<64> Board::getAllBlack()const{
	bitset<64> temp = white; temp.flip();
	return (occupied & (temp));
}

bitset<64> Board::getAllWhite()const{
	return (occupied & white);
}

void Board::setBlack(Square square){
	occupied.set(square);
	white.reset(square);
}

void Board::setWhite(Square square){
	occupied.set(square);
	white.set(square);
}

void Board::setEmpty(Square square){
	occupied.reset(square);
	white.reset(square);
}

vector<Direction> Board::canReverse(Square square){
	vector<Direction> ret; bool flag;
	if(!isEmpty(square)) return ret;
	if(blacksTurn){
		for(Direction direction = Right;((int)direction)<8;direction = (Direction)(direction+1)){
			flag = false; Square recent = square;
			while(1){
				recent = nextSquare(recent, direction);
				if(recent != OUT_OF_BOUND){
					if(isWhite(recent)){
						flag = true; continue;
					}else if(isBlack(recent) && flag){
						ret.push_back(direction);
					}
				}
				break;
			}
		}
	}else{
		for(Direction direction = Right;((int)direction)<8;direction = (Direction)(direction+1)){
			flag = false; Square recent = square;
			while(1){
				recent = nextSquare(recent, direction);
				if(recent != OUT_OF_BOUND){
					if(isBlack(recent)){
						flag = true; continue;
					}else if(isWhite(recent) && flag){
						ret.push_back(direction);
					}
				}
				break;
			}
		}
	}
	return ret;
}

bool Board::haveLegalMove(){
	vector<Direction> dirs;
	for(int i=0;i<60;++i){
		dirs = canReverse(iterateOrder[i]);
		if(!dirs.empty()) return true;
	}
	return false;
}

vector<Square> Board::getLegalMoves(){
	vector<Square> ret; vector<Direction> dirs;
	for(int i=0;i<60;++i){
		dirs = canReverse(iterateOrder[i]);
		if(!dirs.empty()) ret.push_back(iterateOrder[i]);
	}
	return ret;
}

void Board::print()const{
	if(ended){
		printf("Game Ended!\n");
		int bn, wn, result = whoWon(bn, wn);
		printf("Black: %d   White: %d\n", bn, wn);
		switch(result){
			case 1: printf("Black won!\n"); break;
			case 0: printf("Draw QQ\n"); break;
			case -1: printf("White won!\n"); break;
		}	
	}else{
		printf("%s's Turn\n", (blacksTurn)? "Black":"White");
		for(int i=0, who=-1;i<8;++i){
			for(int j=0;j<8;++j) printf("%d ", isWho((Square)++who));
			printf("\n");
		}
	}
}

bool Board::changeBoard(Square square){
	vector<Direction> dirs = canReverse(square);
	if(dirs.empty()) return false;
	int length = dirs.size();
	if(blacksTurn){
		setBlack(square);
		for(int i=0;i<length;++i){
			Square recent = nextSquare(square, dirs[i]);
			while(isWhite(recent)){
				setBlack(recent);
				recent = nextSquare(recent, dirs[i]);
			}
		}		
	}else{
		setWhite(square);
		for(int i=0;i<length;++i){
			Square recent = nextSquare(square, dirs[i]);;
			while(isBlack(recent)){
				setWhite(recent);
				recent = nextSquare(recent, dirs[i]);
			}
		}
	}
	reverseTurn();
	return true;
}
