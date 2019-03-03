import sys 
import random
import copy
import time

class Bot:
	def __init__(self):
		self.start = 0
		self.timeup =0
		self.time_limit = 23
		self.streak = 0

		self.draw_penalty = -10000

		self.focus1 = 6
		self.focus2 = 7

		self.oppfocus1 = 6
		self.oppfocus2 = 7

		self.viscnt = 0

	
		self.triplets = [[(0,0),(0,1),(0,2)], #0 Top Row
						[(2,0),(2,1),(2,2)],  #1 Bottom Row
						[(0,0),(1,0),(2,0)],  #2 Left Col
						[(0,2),(1,2),(2,2)],  #3 Right Col
						[(0,1),(1,1),(2,1)],  #4 Middle Col
						[(1,0),(1,1),(1,2)],  #5 Middle Row
						[(0,0),(1,1),(2,2)],  #6 NW to SE Diag
						[(0,2),(1,1),(2,0)]]  #7 NE to SW Diag


		self.decay = {}
		self.decay[(0,0)] = [(0,1), (0,2), (1,0), (2,0), (1,1), (2,2)]
		self.decay[(0,1)] = [(0,0), (0,2), (1,1), (2,1)]
		self.decay[(0,2)] = [(0,0), (0,1), (1,2), (2,2), (1,1), (2,0)]
		self.decay[(1,0)] = [(1,1), (1,2), (0,0), (0,2)]
		self.decay[(1,1)] = [(i,j) for i in range(3) for j in range(3) if i!=j]
		self.decay[(1,2)] = [(1,0), (1,1), (0,2), (2,2)]
		self.decay[(2,0)] = [(0,0), (1,0), (2,1), (2,2), (1,1), (0,2)]
		self.decay[(2,1)] = [(0,1), (1,1), (2,0), (2,2)]
		self.decay[(2,2)] = [(0,0), (1,1), (0,2), (1,2), (2,0), (2,1)]

		
		print("hello")

	def marker2player(self, s):
		return 0 if s=='x' else 1

	def player2marker(self, s):
		return 'x' if s==0 else 'o'

	def opp(self, flag):
		return 'o' if flag =='x' else 'x'

	def eval_small(self, flag, board, b_no, pos):
		oppflag = self.opp(flag)
		c1 = 3*pos[0]
		c2 = 3*pos[1]

		cnt1 = 0
		cnt2 = 0
		for tri in xrange(len(self.triplets)):
			p = [board.big_boards_status[b_no][i[0]+c1][i[1]+c2] for i in self.triplets[tri]]
			if oppflag in p:
				continue
			if p.count(flag) == 2:
				cnt2+=1
			elif p.count(flag) == 1:
				cnt1+=1

		return 20*cnt2 + 10*cnt1


	def heuristic(self, flag, board, debug = 0):
		oppflag = self.opp(flag)

		tot = 0

		#Mine
		max_val = 0
		max_ind = self.focus1

		for tri in xrange (len(self.triplets)):
			p = [board.small_boards_status[0][i[0]][i[1]] for i in self.triplets[tri]]
			if oppflag in p:
				continue

			my_val = 0

			for i in xrange (len(p)):
				if p[i] == flag:
					my_val += 1000
				else:
					my_val += self.eval_small(flag, board, 0, self.triplets[tri][i])


			if max_val <= my_val:
				max_val = my_val
				max_ind = tri
		
		self.focus1 = max_ind
		tot += max_val

		max_val = 0
		max_ind = self.focus2

		for tri in xrange (len(self.triplets)):
			p = [board.small_boards_status[1][i[0]][i[1]] for i in self.triplets[tri]]
			if oppflag in p:
				continue

			my_val = 0

			for i in xrange (len(p)):
				if p[i] == flag:
					my_val += 1000
				else:
					my_val += self.eval_small(flag, board, 1, self.triplets[tri][i])


			if max_val <= my_val:
				max_val = my_val
				max_ind = tri
		
		self.focus2 = max_ind
		tot += max_val

		#Opponent's
		flag, oppflag = oppflag,flag
		max_val = 0
		max_ind = self.oppfocus1

		for tri in xrange (len(self.triplets)):
			p = [board.small_boards_status[0][i[0]][i[1]] for i in self.triplets[tri]]
			if oppflag in p:
				continue

			my_val = 0

			for i in xrange (len(p)):
				if p[i] == flag:
					my_val += 1000
				else:
					my_val += self.eval_small(flag, board, 0, self.triplets[tri][i])


			if max_val <= my_val:
				max_val = my_val
				max_ind = tri
		
		self.oppfocus1 = max_ind
		tot -= max_val

		max_val = 0
		max_ind = self.oppfocus2

		for tri in xrange (len(self.triplets)):
			p = [board.small_boards_status[1][i[0]][i[1]] for i in self.triplets[tri]]
			if oppflag in p:
				continue

			my_val = 0

			for i in xrange (len(p)):
				if p[i] == flag:
					my_val += 1000
				else:
					my_val += self.eval_small(flag, board, 1, self.triplets[tri][i])


			if max_val <= my_val:
				max_val = my_val
				max_ind = tri
		
		self.oppfocus2 = max_ind
		tot -= max_val


		return tot		


	def update(self, board, old_move, new_move, player):
		ply = self.player2marker(player)
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


	def minimax(self, board, maxDepth, old_move, streak):

		def cut_off(depth):
			if self.timeup or \
			   time.time() - self.start >= self.time_limit:
			    self.timeup = True
			    return True
			if depth > maxDepth:
				return True
			return False


		def maximize(alpha,beta,depth,old_move,streak):
			isGoal = board.find_terminal_state()
			self.viscnt += 1

			if isGoal[1] == "WON":
				if self.marker2player(isGoal[0]) == self.me:
					# board.print_board()
					return float("inf")
				else:
					return float("-inf")

			if cut_off(depth):
				return self.heuristic(self.player2marker(self.me), board)

			v = float("-inf")

			valid_moves = board.find_valid_move_cells(old_move)
			moves_sort = []
			for move in valid_moves:
				self.update(board,old_move,move,self.player2marker(self.me))
				util = self.heuristic(self.player2marker(self.me),board, 0)
				moves_sort.append((util,move))
				board.big_boards_status[move[0]][move[1]][move[2]] = '-'
				board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'

			moves_sort.sort(reverse = True)
			actions = [u[1] for u in moves_sort]			

			for a in actions:
				won = self.update(board, old_move, a,self.me)
				if won and not streak:
					v = max(v,maximize(alpha,beta,depth+1,a,1))
				else:
					v = max(v,minimize(alpha,beta,depth+1,a,0))


				board.big_boards_status[a[0]][a[1]][a[2]] = '-'
				board.small_boards_status[a[0]][a[1]/3][a[2]/3] = '-'

				# print("I played ", a, " util ",v)

				if v>= beta:
					# print(v," beta breaking ",beta)
					return v

				alpha = max(alpha,v)


			return v

		def minimize(alpha,beta,depth,old_move,streak):
			isGoal = board.find_terminal_state()
			self.viscnt += 1

			if isGoal[1] == "WON":
				if self.marker2player(isGoal[0]) == self.me:
					return float("inf")
				else:
					return float("-inf")

			if cut_off(depth):
				return self.heuristic(self.player2marker(self.me), board)



			v = float("inf")
			
			valid_moves = board.find_valid_move_cells(old_move)
			moves_sort = []
			for move in valid_moves:
				self.update(board,old_move,move,self.player2marker(1-self.me))
				util = self.heuristic(self.player2marker(self.me),board, 0)
				moves_sort.append((util,move))
				board.big_boards_status[move[0]][move[1]][move[2]] = '-'
				board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'

			moves_sort.sort()
			actions = [u[1] for u in moves_sort]			

			for a in actions:
				won = self.update(board, old_move, a, 1-self.me)
				if won and not streak:
					v = min(v,minimize(alpha,beta,depth+1,a,1))
				else:
					v = min(v,maximize(alpha,beta,depth+1,a,0))

				board.big_boards_status[a[0]][a[1]][a[2]] = '-'
				board.small_boards_status[a[0]][a[1]/3][a[2]/3] = '-'

				# print("He played ", a, " util ",v)

				if v <= alpha:
					# print(v," alpha breaking",alpha)
					return v

				beta = min(beta,v)

			return v

		best = float("-inf")
		beta = float("inf")

		valid_moves = board.find_valid_move_cells(old_move)
		moves_sort = []
		for move in valid_moves:
			self.update(board,old_move,move,self.player2marker(self.me))
			util = self.heuristic(self.player2marker(self.me),board, 0)
			moves_sort.append((util,move))
			board.big_boards_status[move[0]][move[1]][move[2]] = '-'
			board.small_boards_status[move[0]][move[1]/3][move[2]/3] = '-'

		moves_sort.sort(reverse = True)
		actions = [u[1] for u in moves_sort]			

		best_move = actions[0]
		for a in actions:
			won = self.update(board, old_move, a, self.me)
			if won and not streak:
				v = maximize(best,beta,1,a,1)
			else:
				v = minimize(best,beta,1,a,0)
			
			# print("I played ", a, " util ",v)
			if v > best:
				# print(v," Improved ",best)
				best = v
				best_move = copy.deepcopy(a)


			board.big_boards_status[a[0]][a[1]][a[2]] = '-'
			board.small_boards_status[a[0]][a[1]/3][a[2]/3] = '-'

			if self.timeup or \
			   time.time() - self.start >= self.time_limit:
			    self.timeup = True
			    break


		return best,best_move	


	def move(self, board, old_move, flag):

		self.start = time.time()
		self.timeup = False


		valid = board.find_valid_move_cells(old_move)
		bestMove = valid[0]
		heurmax = 0

		self.me = self.marker2player(flag)
		depth = 1

		original_board = copy.deepcopy(board)

		viscnt = 0
	
		while(True):
			self.viscnt = 0
			move = self.minimax(original_board, depth, old_move, self.streak)		
			if(self.timeup):
				break

			viscnt = self.viscnt
			bestMove = copy.deepcopy(move[1])
			heurmax = move[0]
			depth+=1;

		
		won = self.update(original_board,old_move,bestMove, self.me)
		if won and self.streak == 0:
			self.streak = 1
		else:
			self.streak = 0

		print("Nodes ",self.viscnt)
		print("Depth ",depth)
		print("Heur ",heurmax)
		print("Smartbot played! ",bestMove)
		return bestMove	


