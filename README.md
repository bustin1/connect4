# Connect Four!

![image of connect 4 board](img/connect4.png)  

Connect Four is a classic for kids. The game is played by placing a piece in one of the seven slots
until it lands on another piece. Players alternate turns by placing one piece. 
The objective is to get four in a row/col/diag. The first player
to do this wins. You can play connect four against a computer. 

# Description

The CPU searches 6 depths down by default(can change in source code), and uses the minimax algorithm
with alpha-beta pruning to speed up the process. Still it takes a few seconds to process. 

# Requirements

We need to install some libraries.
```bash
pip install pygame numpy
```
We also need python3 installed

# To play
Run
```bash 
python3 connect4.py
```
