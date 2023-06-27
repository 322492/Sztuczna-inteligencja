#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
import sys
import time

M = 8
DEPTH = 3
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

class Reversi:
    M = 8
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = self.initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(self.M):
            for j in range(self.M):
                if self.board[i][j] is None:
                    self.fields.add((j, i))

    def initial_board(self):
        B = [[None] * self.M for _ in range(self.M)]
        B[3][3] = 1
        B[4][4] = 1
        B[3][4] = 0
        B[4][3] = 0
        return B

    def draw(self):
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = self.board[i][j]
                if b is None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print('')

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player)
                   for direction in self.DIRS):
                res.append((x, y))
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < self.M and 0 <= y < self.M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        assert player == len(self.move_list) % 2
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move is None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player

    def result(self):
        res = 0
        for y in range(self.M):
            for x in range(self.M):
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
        return self.move_list[-1] is None and self.move_list[-2] is None
    
    def my_copy(self):
        # B = copy.deepcopy(self) # slower ~ 15 times
        B = Reversi()
        B.board = [x[:] for x in self.board]
        B.fields = self.fields.copy()
        B.move_list = self.move_list.copy()
        B.history = self.history.copy()
        return B
    
    def heura(self, my_player):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == my_player:
                    res += fields[y][x]
                elif b == 1 - my_player:
                    res -= fields[y][x]
        return res
    
    def corners(self, player):
        res = 0
        for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if self.board[i][j] == player:
                res += 1
        return res
    
    def stability(self, my_player):
        my_res = 0
        opp_res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == my_player:
                    my_res += stabs[y][x]
                elif b == 1 - my_player:
                    opp_res -= stabs[y][x]
        return my_res, opp_res
    
    def heura2(self, player):
        if self.terminal():
            return self.result() * INF

        # difference between my coins and opponent's coins - the more my coins the better
        coin_parity_almost = float(100.0 * self.result()) / (len(self.move_list) + 2)  # procent pionków
        coin_parity = ((len(self.move_list) + 2) > 55) * coin_parity_almost # uwzgledniam tylko koncówkę gry

        # number of different possibilities to move - the more the better
        my_moves = len(self.moves(player))
        opponents_moves = len(self.moves(1 - player))
        mobility = 0
        if my_moves + opponents_moves != 0:
            mobility = float(100 * (my_moves - opponents_moves)) / (my_moves + opponents_moves)

        # numbers of captured corners - the more the better
        my_corners = self.corners(player)
        opponents_corners = self.corners(1 - player)
        corners_captured = 0
        if my_corners + opponents_corners > 0:
            corners_captured = float(100 * (my_corners - opponents_corners) / (my_corners + opponents_corners))

        my_stability, opponent_stability = self.stability(player)
        stability = 0
        if my_stability + opponent_stability != 0:
            stability = float(100 * (my_stability - opponent_stability)) / (abs(my_stability) + abs(opponent_stability))

        #print(coin_parity, mobility, corners_captured, stability)        
        res = coin_parity + mobility + 2 * corners_captured + stability
        return res
    
    def my_move(self, player, start_time):
        def alphabeta(state, depth, alpha, beta, player, start_time):
            if depth == 0 or state.terminal() or time.time() - start_time > 0.9:
                return state.heura(player)

            ms = state.moves(player)
            for move in ms:
                state1 = state.my_copy()
                state1.do_move(move, player)
                if player:
                    alpha = max(alpha, alphabeta(state1, depth-1, alpha, beta, 1 - player, start_time))
                    if alpha >= beta:
                        break
                    return alpha
                else:
                    beta = min(beta, alphabeta(state1, depth-1, alpha, beta, 1 - player, start_time))
                    if alpha >= beta:
                        break
                    return beta
                
            return state.heura(player)
        
        ms = self.moves(player)
        depth = DEPTH
        best_move = (-1, -1)
        best_score = -INF
        for move in ms:
            aux_board = self.my_copy()
            aux_board.do_move(move, player)

            val = alphabeta(aux_board, depth, -INF, INF, 1 - player, start_time)
            if val > best_score:
                best_move = move
                best_score = val

        return best_move


class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Reversi()
        self.my_player = 1
        self.say('RDY')

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def loop(self):
        CORNERS = { (0,0), (0,7), (7,0), (7,7)}
        while True:
            cmd, args = self.hear()
            move_timeout = 0.0
            if cmd == 'HEDID':
                move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1):
                    move = None
                self.game.do_move(move, 1 - self.my_player)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                assert not self.game.move_list
                self.my_player = 0

            start_time = time.time()
            move = self.game.my_move(self.my_player, start_time)
            self.game.do_move(move, self.my_player)
            self.say('IDO %d %d' % move)


if __name__ == '__main__':
    player = Player()
    player.loop()
