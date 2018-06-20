#include "board.hpp"
#include "agent.hpp"
#include <iostream>
#define SIZE 32

char bType[SIZE], wType[SIZE],
	blackIn[SIZE], blackOut[SIZE],
	whiteIn[SIZE], whiteOut[SIZE];

void playGame(Agent &b, Agent &w, int *record){
	Board board; Square move;
	while(!board.isGameEnded()){
		if(!board.haveLegalMove()){
			board.reverseTurn();
			if(!board.haveLegalMove()) board.setGameEnded();
			continue;
		}
		if(board.isBlacksTurn()){
			move = b.getMove(board); ++(record[move]);
		}else{
			move = w.getMove(board); --(record[move]);
		}
		board.changeBoard(move);
	}
}


int main(){
	unsigned int game_per_time, times;
	int bDepth, wDepth, blackLearn; AgentType bT, wT;
	double bRand, wRand, reward;
	printf("black: [Type] [In] [Out] [Depth] [Rand]\nwhite: [Type] [In] [Out] [Depth] [Rand]\n[game/time] [times] [black learn?] [reward]\n");
	bT = readAgentType(); scanf("%s%s%d%lf", blackIn, blackOut, &bDepth, &bRand);
	wT = readAgentType(); scanf("%s%s%d%lf", whiteIn, whiteOut, &wDepth, &wRand);
	scanf("%u%u%d%lf", &game_per_time, &times, &blackLearn, &reward);
	Agent bAgent(true, bT, blackIn, blackOut, bDepth, bRand), wAgent(false, wT, whiteIn, whiteOut, wDepth, wRand);
	int record[64]; Agent *whoLearn = (blackLearn)? &bAgent : &wAgent;
	for(unsigned int i=0;i<times;++i){
		for(int j=0;j<64;++j) record[i] = game_per_time;
		for(unsigned int j=0;j<game_per_time;++j) playGame(bAgent, wAgent, &record[0]);
		printf("%u time over\n", i); fflush(stdout);
		whoLearn->writePriceTable(record, ((blackLearn)? reward:-reward));
	}
	return 0;
}
