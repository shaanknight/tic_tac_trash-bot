import sys 
import random
import copy
import time

class Bot:
	def __init__(self):
		self.start = 0
		self.timeup =0
		self.time_limit = 23

		self.draw_penalty = -10000

		self.score = {}
		self.score["corner_block_won"] = 100
		self.score["centre_block_won"] = 100
		self.score["edge_block_won"] = 50
		
		self.score["corner_cell_won"] = 10
		self.score["centre_cell_won"] = 10
		self.score["edge_cell_won"] = 5
		
		print("hello")

	def marker2player(self, s):
		return 0 if s=='x' else 1

	def player2marker(self, s):
		return 'x' if s==0 else 'o'

	def opp(self, flag):
		return 'o' if flag =='x' else 'x'


	def heuristic(self, flag, board):
		tot = 0
		oppflag = self.opp(flag)

		# CORNER BIG BLOCKS
		tmp = int(board.small_boards_status[0][0][0]==flag) + int(board.small_boards_status[0][2][0]==flag) \
		      + int(board.small_boards_status[0][0][2]==flag) + int(board.small_boards_status[0][2][2]==flag)

		tmp2 = int(board.small_boards_status[1][0][0]==flag) + int(board.small_boards_status[1][2][0]==flag) \
		      + int(board.small_boards_status[1][0][2]==flag) + int(board.small_boards_status[1][2][2]==flag)

		tot += max(tmp,tmp2)*self.score["corner_block_won"]

		tmp = int(board.small_boards_status[0][0][0]==oppflag) + int(board.small_boards_status[0][2][0]==oppflag) \
		      + int(board.small_boards_status[0][0][2]==oppflag) + int(board.small_boards_status[0][2][2]==oppflag)

		tmp2 = int(board.small_boards_status[1][0][0]==oppflag) + int(board.small_boards_status[1][2][0]==oppflag) \
		      + int(board.small_boards_status[1][0][2]==oppflag) + int(board.small_boards_status[1][2][2]==oppflag)

		tot -= max(tmp,tmp2)*self.score["corner_block_won"]

		# CENTER
		tmp = max(int(board.small_boards_status[0][1][1] == flag) , int(board.small_boards_status[1][1][1]==flag))
		tot += tmp * self.score["centre_block_won"]
		
		tmp = max(int(board.small_boards_status[0][1][1] == oppflag) , int(board.small_boards_status[1][1][1]==oppflag))
		tot -= tmp * self.score["centre_block_won"]


		# EDGE 
		tmp = int(board.small_boards_status[0][1][0]==flag) + int(board.small_boards_status[0][0][1]==flag) \
		      + int(board.small_boards_status[0][2][1]==flag) + int(board.small_boards_status[0][1][2]==flag)

		tmp2 = int(board.small_boards_status[1][1][0]==flag) + int(board.small_boards_status[1][0][1]==flag) \
		      + int(board.small_boards_status[1][2][1]==flag) + int(board.small_boards_status[1][1][2]==flag)

		tot += max(tmp,tmp2)*self.score["edge_block_won"]


		tmp = int(board.small_boards_status[0][1][0]==oppflag) + int(board.small_boards_status[0][0][1]==oppflag) \
		      + int(board.small_boards_status[0][2][1]==oppflag) + int(board.small_boards_status[0][1][2]==oppflag)

		tmp2 = int(board.small_boards_status[1][1][0]==oppflag) + int(board.small_boards_status[1][0][1]==oppflag) \
		      + int(board.small_boards_status[1][2][1]==oppflag) + int(board.small_boards_status[1][1][2]==oppflag)

		tot -= max(tmp,tmp2)*self.score["edge_block_won"]

		# print("AT HEUR ",tot)
		# board.print_board()

		return tot

	def update(self, board, old_move, new_move, ply):
		board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply

		x = new_move[1]/3
		y = new_move[2]/3
		k = new_move[0]
		fl = 0

		#checking if a small_board has been won or drawn or not after the current move
		bs = board.big_boards_status[k]
		for i in range(3):
			#checking for horizontal pattern(i'th row)
			if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ply):
				board.small_boards_status[k][x][y] = ply
				return True
			#checking for vertical pattern(i'th column)
			if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ply):
				board.small_boards_status[k][x][y] = ply
				return True
		#checking for diagonal patterns
		#diagonal 1
		if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ply):
			board.small_boards_status[k][x][y] = ply
			return True
		#diagonal 2
		if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ply):
			board.small_boards_status[k][x][y] = ply
			return True
		#checking if a small_board has any more cells left or has it been drawn
		for i in range(3):
			for j in range(3):
				if bs[3*x+i][3*y+j] =='-':
					return False
		board.small_boards_status[k][x][y] = 'd'
		return False

	def minimax(self, board, player, depth, maxDepth, alpha, beta, old_move, streak):

		isGoal = board.find_terminal_state()
		
		if time.time() - self.start > self.time_limit:
			self.timeup = 1
			return (self.heuristic(self.player2marker(self.me),board)), -1

		if isGoal[1] == "WON":
			if self.marker2player(isGoal[0]) == self.me:
				return float("inf"),-1
			else:
				return float("-inf"),-1

		elif isGoal[1] == "DRAW":
			return self.draw_penalty,-1


		if depth == maxDepth:
			return (self.heuristic(self.player2marker(self.me),board)), -1
			


		valid_moves = board.find_valid_move_cells(old_move)
		moves_sort = []
		for move in valid_moves:
			self.update(board,old_move,move,self.player2marker(player))
			util = self.heuristic(self.player2marker(self.me),board)
			moves_sort.append((util,move))
			board.big_boards_status[move[0]][move[1]][move[2]] = '-'
			board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'




		if player == self.me:
		
			moves_sort.sort(reverse = True)
			valid = [u[1] for u in moves_sort]
			maxUtility = float("-inf")
			maxIndex = 0
			# print(valid)

			for i in xrange(len(valid)):
				move = valid[i]
				works = self.update(board,old_move,move,self.player2marker(player))

				childUtility = 0
				if works and not streak:
					childUtility = self.minimax(board,player, depth+1, maxDepth, alpha, beta, move, 1)[0]
				else:
					childUtility = self.minimax(board,1-player, depth+1, maxDepth, alpha, beta, move, 0)[0]

				# print(i," I play ",move," Util ", childUtility)
				if childUtility > maxUtility:
					# print("its bigger")
					maxUtility = childUtility
					maxIndex = i

				alpha = max(alpha, maxUtility)

				board.big_boards_status[move[0]][move[1]][move[2]] = '-'
				board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'

				if alpha >= beta:
					break

			return maxUtility, valid[maxIndex]

		else:

			moves_sort.sort()
			valid = [u[1] for u in moves_sort]
			minUtility = float("inf")
			minIndex = 0

			for i in xrange(len(valid)):
				move = valid[i]
				works = self.update(board,old_move,move,self.player2marker(player))

				childUtility = 0
				if works and not streak:
					childUtility = self.minimax(board,player, depth+1, maxDepth, alpha, beta, move, 1)[0]
				else:
					childUtility = self.minimax(board,1-player, depth+1, maxDepth, alpha, beta, move, 0)[0]

				# print("He plays ",move," Util ", childUtility)
				

				if childUtility < minUtility:
					minUtility = childUtility
					minIndex = i

				beta = min(beta, minUtility)

				board.big_boards_status[move[0]][move[1]][move[2]] = '-'
				board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'

				if beta <= alpha:
					break

			return minUtility, -1







	def move(self, board, old_move, flag):

		self.start = time.time()
		self.timeup = 0

		valid = board.find_valid_move_cells(old_move)
		# print(valid)
		bestMove = valid[0]
		heurmax = 0
		heurind = 0

		self.me = self.marker2player(flag)
		depth = 1


		original_board = copy.deepcopy(board)
	
		while(True):
		# for i in range(1,2):
			# b = copy.deepcopy(board)
			move = self.minimax(original_board,self.me,0,depth,float("-inf"),float("inf"),old_move, False)
			# print(move)
			bestMove = move[1]
			depth+=1;
			if(self.timeup):
				break
			# del b


		print("Depth ",depth)
		print("Smartbot played! ",bestMove)
		return bestMove	


