all:
	g++ -std=c++11 -pthread learn.cpp agent.cpp board.cpp square.cpp -o learn
	g++ -std=c++11 playGUI.cpp agent.cpp board.cpp square.cpp -o playGUI
	g++ -std=c++11 -pthread comPK.cpp agent.cpp board.cpp square.cpp -o PK
learn:
	g++ -std=c++11 -pthread learn.cpp agent.cpp board.cpp square.cpp -o learn
playGUI:
	g++ -std=c++11 playGUI.cpp agent.cpp board.cpp square.cpp -o playGUI
PK:
	g++ -std=c++11 -pthread comPK.cpp agent.cpp board.cpp square.cpp -o PK
clean:
	rm -f playGUI learn PK
