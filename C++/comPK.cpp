#include "board.hpp"
#include "agent.hpp"
#include <mutex>
#include <thread>
using std::thread;
using std::mutex;
#define SIZE 32
#define THREAD_NUMBER 16

#define PRINT(ARGS...) do{printf(ARGS);fflush(stdout);}while(0)

char bType[SIZE], wType[SIZE], blackIn[SIZE], whiteIn[SIZE];
unsigned int game, bWin, wWin, draw;
int bDepth, wDepth, blackLearn; AgentType bT, wT;
mutex gameLock;
thread threads[THREAD_NUMBER];
const int deltaRecord[2][2] = {{-1, 1}, {1, -1}};

void playGame(Agent b, Agent w, int threadId){
	while(1){
		gameLock.lock();
		if(game == 0U){ gameLock.unlock(); break;}
		if((game & 15U) == 0U) PRINT("%u games left\n", game);
		--game; gameLock.unlock();
		Board board; Square move;
		while(!board.isGameEnded()){
			if(!board.haveLegalMove()){
				board.reverseTurn();
				if(!board.haveLegalMove()) board.setGameEnded();
				continue;
			}
			board.changeBoard((board.isBlacksTurn())? b.getMove(board) : w.getMove(board));
		}
		int bn, wn, result; result = board.whoWon(bn, wn);
		switch(result){
			case 1: ++bWin; break;
			case 0: ++draw; break;
			case -1: ++wWin;
		}
	}
}

int main(){
	printf("black: [Type] [In] [Depth]\nwhite: [Type] [In] [Depth]\n[game]\n");
	bT = readAgentType(); scanf("%s%d", blackIn, &bDepth);
	wT = readAgentType(); scanf("%s%d%u", whiteIn, &wDepth, &game);
	Agent bAgent(bT, blackIn, bDepth, 1.0), wAgent(wT, whiteIn, wDepth, 1.0);
	bWin = wWin = draw = 0U;
	for(int k=0;k<THREAD_NUMBER;++k) threads[k] = thread(playGame, bAgent, wAgent, k);
	for(int k=0;k<THREAD_NUMBER;++k) threads[k].join();
	PRINT("bWin: %u  wWin: %u  draw: %u\n", bWin, wWin, draw); exit(0);
}
