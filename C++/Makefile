all:
	g++ -std=c++11 -pthread learn.cpp agent.cpp methods.cpp board.cpp square.cpp -o learn
	g++ -std=c++11 playGUI.cpp agent.cpp methods.cpp board.cpp square.cpp -o playGUI
	g++ -std=c++11 -pthread comPK.cpp agent.cpp methods.cpp board.cpp square.cpp -o PK
	g++ -std=c++11 -pthread comPK_no_thd.cpp agent.cpp methods.cpp board.cpp square.cpp -o PK_no_thd
learn:
	g++ -std=c++11 -pthread learn.cpp agent.cpp methods.cpp board.cpp square.cpp -o learn
playGUI:
	g++ -std=c++11 playGUI.cpp agent.cpp methods.cpp board.cpp square.cpp -o playGUI
PK:
	g++ -std=c++11 -pthread comPK.cpp agent.cpp methods.cpp board.cpp square.cpp -o PK
PK_no_thd:
	g++ -std=c++11 -pthread comPK_no_thd.cpp agent.cpp methods.cpp board.cpp square.cpp -o PK_no_thd
clean:
	rm -f playGUI learn PK
