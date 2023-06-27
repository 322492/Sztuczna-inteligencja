import sys
import math
import random
from copy import deepcopy

INF = 1e9
DEPTH = 5

class Jungle:
    PIECE_VALUES = {
        0: 4,
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 7,
        6: 8,
        7: 10
    }
    MAXIMAL_PASSIVE = 30
    DENS_DIST = 0.1
    MX = 7
    MY = 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}

        for y in range(Jungle.MY):
            for x in range(Jungle.MX):
                C = self.board[y][x]
                if C:
                    pl, pc = C
                    self.pieces[pl][pc] = (x, y)
        self.curplayer = 0
        self.peace_counter = 0
        self.winner = None

    def initial_board(self):
        pieces = """
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """

        B = [x.strip() for x in pieces.split() if len(x) > 0]
        T = dict(zip('rcdwjtle', range(8)))

        res = []
        for y in range(9):
            raw = 7 * [None]
            for x in range(7):
                c = B[y][x]
                if c != '.':
                    if 'A' <= c <= 'Z':
                        player = 1
                    else:
                        player = 0
                    raw[x] = (player, T[c.lower()])
            res.append(raw)
        return res

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in Jungle.ponds and pos2 in Jungle.ponds:
            return True  # rat vs rat
        if pos1 in Jungle.ponds:
            return False  # rat in pond cannot beat any piece on land
        if p1 == Jungle.rat and p2 == Jungle.elephant:
            return True
        if p1 == Jungle.elephant and p2 == Jungle.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in Jungle.traps:
            return True
        return False

    def pieces_comparison(self):
        for i in range(7,-1,-1):
            ps = []
            for p in [0,1]:
                if i in self.pieces[p]:
                    ps.append(p)
            if len(ps) == 1:
                return ps[0]
        return None
                
    def rat_is_blocking(self, player_unused, pos, dx, dy):        
        x, y = pos
        nx = x + dx
        for player in [0,1]:
            if Jungle.rat not in self.pieces[1-player]:
                continue
            rx, ry = self.pieces[1-player][Jungle.rat]
            if (rx, ry) not in self.ponds:
                continue
            if dy != 0:
                if x == rx:
                    return True
            if dx != 0:
                if y == ry and abs(x-rx) <= 2 and abs(nx-rx) <= 2:
                    return True
        return False

    def draw(self):
        TT = {0: 'rcdwjtle', 1: 'RCDWJTLE'}
        for y in range(Jungle.MY):

            L = []
            for x in range(Jungle.MX):
                b = self.board[y][x]
                if b:
                    pl, pc = b
                    L.append(TT[pl][pc])
                else:
                    L.append('.')
            print(''.join(L))
        print('')

    def moves(self, player):
        res = []
        for p, pos in self.pieces[player].items():
            x, y = pos
            for (dx, dy) in Jungle.dirs:
                pos2 = (nx, ny) = (x+dx, y+dy)
                if 0 <= nx < Jungle.MX and 0 <= ny < Jungle.MY:
                    if Jungle.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        if p not in (Jungle.rat, Jungle.tiger, Jungle.lion):
                            continue
                        #if self.board[ny][nx] is not None:
                        #    continue  # WHY??
                        if p == Jungle.tiger or p == Jungle.lion:
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(player, pos, dx, dy):
                                continue
                            pos2 = (nx, ny) = (x+dx, y+dy)
                    if self.board[ny][nx] is not None:
                        pl2, piece2 = self.board[ny][nx]
                        if pl2 == player:
                            continue
                        if not self.can_beat(p, piece2, pos, pos2):
                            continue
                    res.append((pos, pos2))
        return res

    def victory(self, player):
        oponent = 1 - player        
        if len(self.pieces[oponent]) == 0:
            self.winner = player
            return True

        x, y = self.dens[oponent]
        if self.board[y][x]:
            self.winner = player
            return True
        
        if self.peace_counter >= Jungle.MAXIMAL_PASSIVE:
            r = self.pieces_comparison()
            if r is None:
                self.winner = 1 # draw is second player's victory 
            else:
                self.winner = r
            return True
        return False

    def do_move(self, m):
        self.curplayer = 1 - self.curplayer
        if m is None:
            return
        pos1, pos2 = m
        x, y = pos1
        pl, pc = self.board[y][x]
        
        x2, y2 = pos2
        if self.board[y2][x2]:  # piece taken!
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1    

        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y][x] = None
    
    def better_move(self, moves):
        scores = {m: 0 for m in moves}
        best_score = -INF
        
        for m in moves:
            G = deepcopy(self)
            G.do_move(m)
            scores[m] = heura(G)
            best_score = max(best_score, scores[m])

        best_moves = [m for m in moves if scores[m] == best_score]
        if not best_moves:
            return None
        return random.choice(best_moves)
    
    def my_move(self, player):
        def alphabeta(state, depth, alpha, beta, player):
            if depth == 0 or state.victory(1 - state.curplayer):
                return heura4(state)

            ms = state.moves(player)
            for move in ms:
                state1 = deepcopy(state)
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
            game = deepcopy(self)
            game.do_move(move, player)

            val = alphabeta(game, depth, -INF, INF, 1 - player)
            if val > best_score:
                best_move = move
                best_score = val

        return best_move
    
def dist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])

def heura4(game):
    if game.victory(1 - game.curplayer):
        return INF
    score = 0
    opp = game.curplayer
    me = 1 - game.curplayer

    for p, pos in game.pieces[me].items():
        score += p * dist(pos, game.dens[opp])

    for p, pos in game.pieces[opp].items():
        score -= p * dist(pos, game.dens[me])

    opp_dist = min([dist(game.dens[me], game.pieces[opp][piece]) for piece in game.pieces[opp]])
    my_dist = min([dist(game.dens[opp], game.pieces[me][piece]) for piece in game.pieces[me]])
    score = opp_dist - my_dist

    return score

def heura3(game):
    score = 0
    opp = game.curplayer
    me = 1 - game.curplayer

    opp_dist = min([dist(game.dens[me], game.pieces[opp][piece]) for piece in game.pieces[opp]])
    my_dist = min([dist(game.dens[opp], game.pieces[me][piece]) for piece in game.pieces[me]])
    score = opp_dist - my_dist

    return score

def heura2(game):
    score = 0
    opp = game.curplayer
    me = 1 - game.curplayer

    opp_animals = sum([p for p in game.pieces[opp].keys()])
    my_animals = sum([p for p in game.pieces[me].keys()])

    score = my_animals - opp_animals

    return score
    
def heura(game):
    score = 0
    opponent = game.curplayer
    for p, pos in game.pieces[1 - opponent].items():
        score -= p * dist(pos, game.dens[opponent])

    return score

color = input()  # color of your player ("red" or "blue"), red moving first
G = Jungle()
if color == "red":
    G.curplayer = 0
if color == "blue":
    G.curplayer = 1
# game loop
while True:
    # x_1: x-coordinate of a piece to move
    # y_1: y-coordinate of a piece to move
    # x_2: x-coordinate of a destination square
    # y_2: y-coordinate of a destination square
    x_1, y_1, x_2, y_2 = [int(i) for i in input().split()]
    if (x_1, y_1, x_2, y_2) != (-1, -1, -1, -1):
        G.do_move(((x_1, y_1), (x_2, y_2)))
    move_count = int(input())  # number of legal moves
    moves = []
    for i in range(move_count):
        #move = input()  # a legal move
        x_1, y_1, x_2, y_2 = [int(i) for i in input().split()]
        moves.append(((x_1, y_1), (x_2, y_2)))
    m = G.better_move(moves)
    #print(m, file=sys.stderr, flush=True)
    G.do_move(m)
    print(m[0][0], m[0][1], m[1][0], m[1][1])

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # e.g. "1 7 1 6" (move from 1 7 to 1 6) or "random"
    #print("random")
