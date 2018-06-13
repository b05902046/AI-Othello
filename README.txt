分為game, gameState兩個class

game負責繪圖，並且handle遊戲進行
gameState儲存當前board的狀態

Files:
  Othello.py: 最原始的遊戲
  Oth.py: ?
  Oth2.py: 人vs Minimax
  Othello_learn.py: 純learn(沒有GUI)
  newOthello.py:最新的遊戲（play & learn)
  method.py: 不同種agents
  eval.txt: train出的price_table
  eval_old: 初始的price_table
在init game的時候會同時宣告一個gameState（gameState在game裡面）

6/13 14:55:    b05902020 
  執行方式 輸入make後 在輸入兩個整數 [repeat_time][depth_limit] 
    repeat_time == -1   ==>   play mode 
    else   ==>     learn_mode 
