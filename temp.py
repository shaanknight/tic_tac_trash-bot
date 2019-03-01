def move(self, board, old_move, flag):

        self.starttime = time()
        #print self.starttime
        if flag == "x":
            self.max_player = 1
        else:
            self.max_player = 0
        #print self.max_player

        player = self.max_player
        level = self.initial_level
        self.timeup = 0
        self.init_zobrist(board)
        self.num_blks_won = [0 ,0 ]
        if self.last_blk_won :
            self.num_blks_won[self.max_player] = 1

        #print self.blk_hash
        #self.update_zobrist_block(old_move, player^1 , 0)

        #curmax = -self.INF
        self.available_moves = board.find_valid_move_cells(old_move)


        #print self.available_moves
        length = len(self.available_moves)
        prevans = self.available_moves[random.randrange(length)]
        if self.just_start ==1 :
            self.just_start = 0
            return prevans
        while(not self.timeup):
            self.init_zobrist(board)
            ans, val = self.move_minimax(board, old_move, player, level)
           
            self.maxlen = max(self.maxlen, len(self.dict))
            if (self.timeup):
                break;
            prevans = ans
            level += 1

        #print level, self.maxlen
        #self.numsteps += 1
        #self.timeup = 0
        #print "Returned answer"
        status, blk_won = self.update(board, old_move, prevans, self.map_symbol[player])

        if blk_won == True :
            self.last_blk_won ^= 1
        else:
            self.last_blk_won = 0
            # do something 
        board.board_status[prevans[0]][prevans[1]] = "-"
        board.block_status[prevans[0]/4][prevans[1]/4] = "-"
        self.mindepth = min(self.mindepth, level)
        #print self.mindepth, level , time()-self.starttime
        return prevans
        # except Exception as e:
#   print e