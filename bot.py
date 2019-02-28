import sys 
import random
import copy
import time

class Bot:
	def __init__(self):
		self.score = {}
		self.score["corner_block_won"] = 100
		self.score["centre_block_won"] = 100
		self.score["edge_block_won"] = 50
		
		self.score["corner_cell_won"] = 10
		self.score["centre_cell_won"] = 10
		self.score["edge_cell_won"] = 5
		
		print("hello")

	def opp(self, flag):
		return 'o' if flag =='x' else 'x'

	def heuristic(self, flag, board):
		tot = 0


		# CORNER BIG BLOCKS
		tmp = int(board.small_boards_status[0][0][0]==flag) + int(board.small_boards_status[0][2][0]==flag) \
		      + int(board.small_boards_status[0][0][2]==flag) + int(board.small_boards_status[0][2][2]==flag)

		tmp2 = int(board.small_boards_status[1][0][0]==flag) + int(board.small_boards_status[1][2][0]==flag) \
		      + int(board.small_boards_status[1][0][2]==flag) + int(board.small_boards_status[1][2][2]==flag)

		tot += max(tmp,tmp2)*self.score["corner_block_won"]

		tmp = int(board.small_boards_status[0][0][0]==self.opp(flag)) + int(board.small_boards_status[0][2][0]==self.opp(flag)) \
		      + int(board.small_boards_status[0][0][2]==self.opp(flag)) + int(board.small_boards_status[0][2][2]==self.opp(flag))

		tmp2 = int(board.small_boards_status[1][0][0]==self.opp(flag)) + int(board.small_boards_status[1][2][0]==self.opp(flag)) \
		      + int(board.small_boards_status[1][0][2]==self.opp(flag)) + int(board.small_boards_status[1][2][2]==self.opp(flag))

		tot -= max(tmp,tmp2)*self.score["corner_block_won"]

		# CENTER
		tmp = max(int(board.small_boards_status[0][1][1] == flag) , int(board.small_boards_status[1][1][1]==flag))
		tot += tmp * self.score["centre_block_won"]
		
		tmp = max(int(board.small_boards_status[0][1][1] == self.opp(flag)) , int(board.small_boards_status[1][1][1]==self.opp(flag)))
		tot -= tmp * self.score["centre_block_won"]


		# EDGE 
		tmp = int(board.small_boards_status[0][1][0]==flag) + int(board.small_boards_status[0][0][1]==flag) \
		      + int(board.small_boards_status[0][2][1]==flag) + int(board.small_boards_status[0][1][2]==flag)

		tmp = int(board.small_boards_status[1][1][0]==flag) + int(board.small_boards_status[1][0][1]==flag) \
		      + int(board.small_boards_status[1][2][1]==flag) + int(board.small_boards_status[1][1][2]==flag)

		tot += max(tmp,tmp2)*self.score["edge_block_won"]


		tmp = int(board.small_boards_status[0][1][0]==self.opp(flag)) + int(board.small_boards_status[0][0][1]==self.opp(flag)) \
		      + int(board.small_boards_status[0][2][1]==self.opp(flag)) + int(board.small_boards_status[0][1][2]==self.opp(flag))

		tmp = int(board.small_boards_status[1][1][0]==self.opp(flag)) + int(board.small_boards_status[1][0][1]==self.opp(flag)) \
		      + int(board.small_boards_status[1][2][1]==self.opp(flag)) + int(board.small_boards_status[1][1][2]==self.opp(flag))

		tot -= max(tmp,tmp2)*self.score["edge_block_won"]

		
		return tot


	def minimax(self, board, flag, depth, maxDepth, alpha, beta, old_move):
		isGoal = board.find_terminal_state()

		if isGoal[1] == "WON":
			if isGoal[0] == self.who:
				return float('inf'),"placehoder"
			else:
				return float("-inf"),"placeholder"

		elif isGoal[1] == "DRAW":
			return -100000, "placeholder"

		if depth == maxDepth:
			return (self.heuristic(self.who,board)), "placeholder"

		valid = board.find_valid_move_cells(old_move)

		isMax = (flag == self.who)

		if isMax:
			maxVal = float("-inf")
			maxInd = 0

			for i in xrange(len(valid)):
				cell = valid[i]
				isSuccess = board.update(old_move, cell, flag)

				val = 0
				if(isSuccess[0] == "SUCCESSFUL" and isSuccess[1] == True):
					val = self.minimax(board,flag, depth+1,maxDepth,alpha,beta,cell)[0]
				else:
					val = self.minimax(board,self.opp(flag), depth+1,maxDepth,alpha,beta,cell)[0]

				if val > maxVal:
					maxVal = val
					maxInd = i
				if maxVal > alpha:
					alpha = maxVal

				board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
				board.small_boards_status[cell[0]][cell[1]%3][cell[2]%3] = '-'

				if beta <= alpha:
					break

			return maxVal, valid[maxInd]

		else:
			minVal = float("inf")
			minInd = 0

			for i in xrange(len(valid)):
				cell = valid[i]
				board.update(old_move, cell, flag)

				val = self.minimax(board,self.opp(flag), depth+1,maxDepth,alpha,beta,cell)[0]

				if val < minVal:
					minVal = val
					minInd = i
				if minVal < beta:
					beta = minVal

				board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
				board.small_boards_status[cell[0]][cell[1]%3][cell[2]%3] = '-'

				if beta <= alpha:
					break

			return minVal, "placeholder"




	def move(self, board, old_move, flag):
		valid = board.find_valid_move_cells(old_move)
		# print(valid)
		bestMove = valid[0]

		self.who = flag
		depth = 5
		start = time.time()
		for i in range(1,depth):
			b = copy.deepcopy(board)
			move = self.minimax(b,flag,0,depth,float("-inf"),float("inf"),old_move)
			# print(move)
			bestMove = move[1]
			del b

		end = time.time()

		print ("time ",end-start)

		# print("I played! ",move)
		return bestMove	


