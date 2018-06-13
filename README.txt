分為game, gameState兩個class

game負責繪圖，並且handle遊戲進行
gameState儲存當前board的狀態

在init game的時候會同時宣告一個gameState（gameState在game裡面）

6/13 14:55:    b05902020 
  執行方式 輸入make後 在輸入兩個整數 [repeat_time][depth_limit] 
    repeat_time == -1   ==>   play mode 
    else   ==>     learn_mode 
