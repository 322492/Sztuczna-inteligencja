from queue import PriorityQueue
from queue import Queue
import copy

board = []
dict_positions = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
dict_positions_opposites = {'R': 'L', 'D': 'U', 'L': 'R', 'U': 'D'}
dists = []
destinations = set()

def calculate_pos(positions, direction):
    new_pos = set()
    x = dict_positions[direction]
    
    for pos in positions:
        np = (pos[0] + x[0], pos[1] + x[1])
        if(board[np[0]][np[1]] == '#'):
            new_pos.add(pos)
        else:
            new_pos.add(np)
    return new_pos

def create_data(): # making starting positions and dists arrays

    positions = set()
    global dists
    
    n = len(board)
    m = len(board[0])
    MAX = n * m
    dists = [[MAX] * m for _ in range(n)]
    Q = Queue()
    vis = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'S':
                positions.add((i, j))
                dists[i][j] = MAX
            if board[i][j] == 'B':
                positions.add((i, j))
                destinations.add((i, j))
                dists[i][j] = 0
                Q.put((i, j, 0))
            if board[i][j] == 'G':
                dists[i][j] = 0
                destinations.add((i, j))
                Q.put((i, j, 0))

    while not Q.empty():
        (x, y, c) = Q.get()

        vis.add((x, y))
        for d in dict_positions:
            (nx, ny) = (x + dict_positions[d][0], y + dict_positions[d][1])
            if(board[nx][ny] != '#'):
                if (nx, ny) not in vis:
                    dists[nx][ny] = min(dists[nx][ny], c + 1)
                    Q.put((nx, ny, min(dists[nx][ny], c + 1)))
                    vis.add((nx, ny))
    
    return positions

'''
in fourth program there were
mean 1402, 1436, 1357 total num-moves and
mean 7.2,  12.1, 15.8 total time

in this program I have:
mean 728, 728, 728 total num-moves and
mean 3.2, 2.8, 3.6 total time
'''

# this works
def heura(positions):
    return sum(dists[x][y] for (x, y) in positions) * 0.7

# one time worked, in others one tests is too slow
def heura1(positions):
    epsilon = 7
    return (1 + epsilon) * max(dists[x][y] for (x, y) in positions)

def is_end(positions):
    for (x, y) in positions:
        if (x, y) not in destinations:
            return False
    return True

def BFS(positions):

    Visited = set()
    Q = PriorityQueue() # (distance, result_length, state, result)
    # withouth result_length sometimes path is slighty longer than optimal, I think that because we also want to prioritize length of result
    dist = heura(positions)
    if dist == 0:
        return " "
    Q.put((dist, 0, positions, " "))
    
    while not Q.empty():
        (dist, res_len, state, res) = Q.get()
        Visited.add(frozenset(state))
        for move in dict_positions:
            new_state = calculate_pos(state, move)
            if new_state not in Visited:
                if is_end(new_state):
                    return res[1:] + move
                new_dist = heura(new_state)
                Q.put((len(res) + new_dist, len(res), new_state, res + move))
                Visited.add(frozenset(new_state))
    return ""

def solve():
    positions = create_data()
    res = BFS(positions)
    return res

if __name__ == '__main__':
    input = open('zad_input.txt').readlines()
    board = [line for line in input]

    with open('zad_output.txt', mode='w') as out_file:
        out_file.write(solve())