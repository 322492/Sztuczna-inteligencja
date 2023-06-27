import random
import sys
from collections import defaultdict as dd
import copy
import time

M = 8
number_games = 1000
DEPTH = 0
INF = 1e9

fields = ((100, -10, 11, 6, 6, 11, -10, 100),
           (-10, -20,  1, 2, 2, 1, -20, -10),
           (10,   1,   5, 4, 4, 5,  1,  10),
           (6,    2,   4, 2, 2, 4,  2,   6),
           (6,    2,   4, 2, 2, 4,  2,   6),
           (10,   1,   5, 4, 4, 5,  1,  10),
           (-10, -20,  1, 2, 2, 1, -20, -10),
           (100, -10, 11, 6, 6, 11, -10, 100))

stabs =  ((4,  -3,   2,  2,  2,  2, -3,  4),
          (-3, -4,  -1, -1, -1, -1, -4, -3),
          (2,  -1,   1,  0,  0,  1, -1,  2),
          (2,  -1,   0,  1,  1,  0, -1,  2),
          (2,  -1,   0,  1,  1,  0, -1,  2),
          (2,  -1,   1,  0,  0,  1, -1,  2),
          (-3, -4,  -1, -1, -1, -1, -4, -3),
          (4,  -3,   2,  2,  2,  2, -3,  4))

def initial_board():
    B = [ [None] * M for i in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B

class Board:
    dirs  = [ (0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]
    
    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == None:   
                    self.fields.add( (j,i) )
                                                
    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b == None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print (''.join(res))
        print            
        
    def moves(self, player):
        res = []
        for (x,y) in self.fields:
            if any( self.can_beat(x,y, direction, player) for direction in Board.dirs):
                res.append( (x,y) )
        if not res:
            return [None]
        return res               
    
    def can_beat(self, x,y, d, player):
        dx,dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x,y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x,y) == player
    
    def get(self, x,y):
        if 0 <= x < M and 0 <=y < M:
            return self.board[y][x]
        return None
                        
    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)
        
        if move == None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx,dy in self.dirs:
            x,y = x0,y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x,y) == 1 - player:
              to_beat.append( (x,y) )
              x += dx
              y += dy
            if self.get(x,y) == player:              
                for (nx,ny) in to_beat:
                    self.board[ny][nx] = player
                                                     
    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]                
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res
                
    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]
    
    def my_copy(self):
        # B = copy.deepcopy(self) # slower ~ 15 times
        B = Board()
        B.board = [x[:] for x in self.board]
        B.fields = self.fields.copy()
        return B
    
    def heura(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == 0:
                    res += fields[y][x]
                elif b == 1:
                    res -= fields[y][x]
        return res
    
    def corners(self, player):
        res = 0
        for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if self.board[i][j] == player:
                res += 1
        return res
    
    def stability(self):
        my_res = 0
        opp_res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == 0:
                    my_res += stabs[y][x]
                elif b == 1:
                    opp_res -= stabs[y][x]
        return my_res, opp_res
    
    def heura2(self):
        if self.terminal():
            return self.result() * INF

        # difference between my coins and opponent's coins - the more my coins the better
        coin_parity_almost = float(100.0 * self.result()) / (len(self.move_list) + 2)  # procent pionków
        coin_parity = ((len(self.move_list) + 2) > 55) * coin_parity_almost # uwzgledniam tylko koncówkę gry

        # number of different possibilities to move - the more the better
        my_moves = len(self.moves(0))
        opponents_moves = len(self.moves(1))
        mobility = 0
        if my_moves + opponents_moves != 0:
            mobility = float(100 * (my_moves - opponents_moves)) / (my_moves + opponents_moves)

        # numbers of captured corners - the more the better
        my_corners = self.corners(0)
        opponents_corners = self.corners(1)
        corners_captured = 0
        if my_corners + opponents_corners > 0:
            corners_captured = float(100 * (my_corners - opponents_corners) / (my_corners + opponents_corners))

        my_stability, opponent_stability = self.stability()
        stability = 0
        if my_stability + opponent_stability != 0:
            stability = float(100 * (my_stability - opponent_stability)) / (abs(my_stability) + abs(opponent_stability))

        #print(coin_parity, mobility, corners_captured, stability)        
        res = coin_parity + mobility + 2 * corners_captured + stability
        return res

    def my_move(self, player):
        def alphabeta(state, depth, alpha, beta, player):
            if depth == 0 or state.terminal():
                return state.heura()

            ms = state.moves(player)
            for move in ms:
                state1 = state.my_copy()
                state1.do_move(move, player)
                if player:
                    alpha = max(alpha, alphabeta(state1, depth-1, alpha, beta, 1 - player))
                    if alpha >= beta:
                        break
                    return alpha
                else:
                    beta = min(beta, alphabeta(state1, depth-1, alpha, beta, 1 - player))
                    if alpha >= beta:
                        break
                    return beta
        
        ms = self.moves(player)
        depth = DEPTH
        best_move = None
        best_score = -INF
        for move in ms:
            aux_board = self.my_copy()
            aux_board.do_move(move, player)

            val = alphabeta(aux_board, depth, -INF, INF, 1 - player)
            if val > best_score:
                best_move = move
                best_score = val

        return best_move

win, tie, lost = 0, 0, 0
start = time.time()
for i in range(number_games):
        if i % (number_games/10) == 0:
            print("%d games (%d-%d-%d) %f" %(i, win, tie, lost, time.time() - start))
        player = random.randint(0, 1) # 1 - random, 0 - I
        B = Board()

        while True:
            if player:
                m = B.random_move(player)
            else:
                m = B.my_move(player)
            B.do_move(m, player)
            player = 1 - player
            if B.terminal():
                break

        if B.result() < 0:
            win += 1
        elif B.result() == 0:
            tie += 1
        else:
            lost += 1

end = time.time()
print("Duration of experiment: ", end - start)
print("Number of games: ", number_games)
print("I won-tied-lost %d-%d-%d times." %(win, tie, lost))