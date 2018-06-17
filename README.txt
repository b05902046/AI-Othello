分為game, gameState兩個class

game負責繪圖，並且handle遊戲進行
gameState儲存當前board的狀態

Files:
  Othello.py: 最原始的遊戲
  Oth.py: ?
  Oth2.py: 人vs Minimax
  Othello_learn.py: 純learn(沒有GUI) input: （repeat, depth, opponent file path, learner file path)
  newOthello.py:最新的遊戲 input:（play: -1, depth, file path ; learn: repeat, depth, opponent file path, learner file path)
  method.py: 不同種agents
  eval.txt: train出的price_table
  eval_old: 初始的price_table
  input: 將此檔案重導向給Othello_learn.py 會讓先手使用eval_old.txt作為price_table，後手則是使用eval.txt(只有後手會learn)

在init game的時候會同時宣告一個gameState（gameState在game裡面）

6/13 14:55:    b05902020 
  執行方式 輸入make後 在輸入兩個整數 [repeat_time][depth_limit] 
    repeat_time == -1   ==>   play mode 
    else   ==>     learn_mode 

6/14 19:35:    b05902016
  執行./Othello_learn.py < input 即可
  仍然會出現illegal move??????
  Othello_learn.py的game的class裡面有兩個price_table及兩個evaluation file的檔名，並將wmoves, bmoves, nobody整合到class中
  可能還有bug～～～～～～～～

6/16 11:24:    b05902016
  解決了./Othello_learn.py < input在expand node時回傳illegal move的情形
  將method.py其中一方勝利時的回傳值改為810000或-810000，避免>float('inf')或是<float('-inf')的情形發生
  
