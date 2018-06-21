分為game, gameState兩個class

game負責繪圖，並且handle遊戲進行
gameState儲存當前board的狀態

Files:
  Othello.py: 最原始的遊戲
  Othello_learn.py: 純learn(沒有GUI) input: （repeat, depth, opponent file path, learner file path)
  Othello_playmode.py:人對電腦 input:（play: depth, file path) 
  method.py: 不同種agents
  eval: price table 的資料夾
  GUI.py: 協助C++繪圖
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
  
6/19 18:29:  b05902020 
  更新C++可call python GUI.py進行繪圖
  make learn ==> 學習用 
  make playGUI ==> 進行遊戲 
    支援真人和電腦共四種玩法 
  ----------願景-----------
  1.用multithread學習, 因為一次學習會先下很多場, 
  可以讓多場同時進行！ 
  2.多做一種搜尋方式 -> 改進alpha_beta: 
    (1)記住上一次搜尋的最佳路徑, 下一次優先考慮此發展, 剪枝效果up! 
    (2)將子節點分為三種類型的局面(好, 普通, 壞) 
    
