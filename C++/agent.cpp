#include "agent.hpp"
#include <string.h>
#include <cstdlib>

char defaultFileName[5] = "eval";
std::default_random_engine generator;
char buf[32];
#ifdef WATCH_NODE
extern unsigned long long int nodeSearched, totalNodeSearched;
#endif

AgentType readAgentType(){
	scanf("%s", buf);
	if(strcmp(buf, "AB") == 0) return ALPHA_BETA;
	else if(strcmp(buf, "ABR") == 0) return ALPHA_BETA_RAND;
	else if(strcmp(buf, "H") == 0) return ALPHA_BETA_HIS;
	else if(strcmp(buf, "R") == 0) return ALPHA_BETA_HIS_RAND;
	else if(strcmp(buf, "PLAYER") == 0) return PLAYER;
	else{ printf("Wrong agent type: %s\n", buf); exit(1);}
}

void printAgentType(AgentType type){
	switch(type){
		case PLAYER: printf("type: PLAYER\n"); break;
		case ALPHA_BETA: printf("type: ALPHA_BETA\n"); break;
		case ALPHA_BETA_RAND: printf("type: ALPHA_BETA_RAND\n"); break;
		default: printf("type: DEFAULT\n");
	}
}

int randInt(int N){
	std::uniform_int_distribution<int> distribution(0, N-1);
	return distribution(generator);
}

double randReal(){	std::uniform_real_distribution<double> distribution(0.0, 1.0);
	return distribution(generator);
}

void Agent::setEvalNames(char *a, char *b){
	readEvalName = a; writeEvalName = b;
}

void Agent::getPriceTable(){
	const char *str = readEvalName.c_str();	FILE *fp = fopen(str, "r");
	if(fp == NULL){ printf("getPriceTable: Failed to open %s\n", str); exit(1);}
	double *p = priceTable;
	for(int i=0;i<64;i+=8) fscanf(fp, "%lf%lf%lf%lf%lf%lf%lf%lf", &p[i], &p[i+1], &p[i+2], &p[i+3], &p[i+4], &p[i+5], &p[i+6], &p[i+7]);
	fclose(fp);
}

Square Agent::getBestMove(Board &board){
	sucInform result; int num; vector<Square> legalMoves;
	if(isRandom && (randReal() > rand)){
		legalMoves = board.getLegalMoves(); num = legalMoves.size();
		return legalMoves[randInt(num)];
	}
	switch(type){
		case ALPHA_BETA:
		case ALPHA_BETA_RAND:
			#ifdef WATCH_NODE
			nodeSearched = 0ULL;
			#endif
			result = alphaBeta(board, MINF, INF, 0, false);
			#ifdef WATCH_NODE
			printf("nodeSearched = %llu\n", nodeSearched);
			totalNodeSearched += nodeSearched;
			#endif
			if((num = result.moves.size()) == 0){ printf("alphaBeta returned empty moves!\n"); exit(1);}
			return result.moves[randInt(num)];
		//case ALPHA_BETA_HIS:
		//case ALPHA_BETA_HIS_RAND:
			/*






			*/
		//	break;
		default:
			printf("Failed at getBestMove:  no such agent type\n"); exit(1);
	}
}

Square Agent::playerGetMove(Board &board){
	vector<Square> legalMoves = board.getLegalMoves();
	int num = legalMoves.size(), iRead, jRead;
	for(int i=0;i<num;++i) printf("(%d %d) ", getI(legalMoves[i])+1, getJ(legalMoves[i])+1);
	while(1){
		scanf("%d%d", &iRead, &jRead); --iRead; --jRead;
		if(!outOfBound(iRead, jRead)) return getSquare(iRead, jRead);
		else printf("Invalid move!\n");
	}
}

Agent::Agent(){
	type = PLAYER;
	//getMoveFunction = std::bind(&Agent::playerGetMove, this, std::placeholders::_1);
}

Agent::Agent(const AgentType &which, char *readFileName = NULL, int depthL = 5, double ran = 0.7){
	if((type = which) != PLAYER){
		isRandom = (type == ALPHA_BETA_RAND || type == ALPHA_BETA_HIS_RAND)? true:false;
		depthLimit = depthL; rand = ran;
		setEvalNames(readFileName, readFileName);
		getPriceTable();
		//getMoveFunction = std::bind(&Agent::getBestMove, this, std::placeholders::_1);
	}//else getMoveFunction = std::bind(&Agent::playerGetMove, this, std::placeholders::_1);
}

Agent::Agent(const AgentType &which, char *readFileName, char *writeFileName, int depthL, double ran){
	type = which; depthLimit = depthL; rand = ran;
	isRandom = (type == ALPHA_BETA_RAND || type == ALPHA_BETA_HIS_RAND)? true:false;
	setEvalNames(readFileName, writeFileName); getPriceTable();
	//if(type == PLAYER) std::bind(&Agent::playerGetMove, this, std::placeholders::_1);
	//else std::bind(&Agent::getBestMove, this, std::placeholders::_1);
}

void Agent::print(){
	printAgentType(type);
	if(type != PLAYER) printf("read: %s   write: %s  depth limit = %d\n", readEvalName.c_str(), writeEvalName.c_str(), depthLimit);
	//print price_table?
}

void Agent::writePriceTable(int *array, double re){
	const char *str = writeEvalName.c_str(); FILE *fp = fopen(str, "w");
	if(fp == NULL){ printf("writePriceTable: Failed to open %s\n", str); exit(1);}
	double *p = priceTable, total = 0.0;
	for(int i=0;i<64;++i){
		p[i] += re * array[i]; total += p[i];
	}
	total /= 64;
	for(int i=0;i<64;i+=8)
		fprintf(fp, "%lf %lf %lf %lf %lf %lf %lf %lf\n", p[i]/total, p[i+1]/total, p[i+2]/total,
				p[i+3]/total, p[i+4]/total, p[i+5]/total, p[i+6]/total, p[i+7]/total);
	fflush(fp);	fclose(fp);
}

double Agent::evaluateBoard(const Board &board){
	double ret = 0.0;
	bitset<64> black = board.getAllBlack(), white = board.getAllWhite();
	for(int i=0;i<64;++i){
		if(white[i]) ret -= priceTable[i];
		else if(black[i]) ret += priceTable[i];
	}
	return ret;
}

Square Agent::getMove(Board &board){
        return ((type == PLAYER)? playerGetMove(board):getBestMove(board));
}


/*

int main(){
	Agent agent3(ALPHA_BETA_RAND, "eval3");
	agent3.print();
	Board board;
	for(int i=0;i<16;++i){
		printSquare(agent3.getBestMove(board));
	}
	return 0;
}
*/
