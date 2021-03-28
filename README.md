# Tic-Tac-Trash Bot
### Contributors : C Athreya, Sayantan Jana 
A bot that plays a variation of ultimate tic tac toe, called Xtreme tic tac toe. The details of the game and the rules can be found in `Description.pdf`. 

The project was created for the course on Artificial Intelligence in Spring 2019. The bot placed 5th among 74 bots in an intra-batch tournament. Analysis of a few games can be found in `Analysis.pdf`. The rules for the tournament can also be found in `Description.pdf`.

It implements Minimax Search with alpha-beta pruning and query reordering. Uses an adaptive heuristic that changes expected utilities based on the state of the game.

## To Run
- Replace `obj2` in `simulator.py` with either a human, random or another bot(import the class first)
- Run `simulator.py` with python3
