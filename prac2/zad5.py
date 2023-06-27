from queue import PriorityQueue
from queue import Queue
import copy

board = []
dict_positions = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
dict_positions_opposites = {'R': 'L', 'D': 'U', 'L': 'R', 'U': 'D'}
dists = []
destinations = set() # I don't really need it now

def print_board(brd, positions):
    b = ""
    for i in range(len(brd)):
        line = ""
        for j in range(len(brd[i])):
            if(board[i][j] == '#'):
                line += "#"
            elif((i, j) in positions):
                line += 'S'
            elif board[i][j] == 'G':
                line += 'G'
            else:
                line += ' '
        b+= line + "\n"

    print(b)

def pretty_print(brd):
    b = ""
    for i in range(len(brd)):
        line = ""
        for j in range(len(brd[i])):
            if(board[i][j] == '#'):
                line += "# "
            else:
                line += str(brd[i][j]) + " "
        b += line + "\n"
    return b

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

def opposite(x):
    if(x not in dict_positions_opposites):
        return x
    return dict_positions_opposites[x]

def analise(positions, res, dists):
    print(res)
    brd = copy.deepcopy(board)
    print_board(brd, positions)
    for c in res:
        print(c)
        print(heura(positions, dists))
        positions = calculate_pos(positions, c)
        print_board(brd, positions)

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
                #destinations.add((i, j))
                dists[i][j] = 0
                Q.put((i, j, 0))
            if board[i][j] == 'G':
                dists[i][j] = 0
                #destinations.add((i, j))
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

# based on BFS distaance from destinations
def heura(positions):
    return max(dists[x][y] for (x, y) in positions)

# based on manhattan distance from destinations - take much longer time and don't pass all tests, only 15/21. Needs destinations set created
def heura1(positions):
    res = 0
    for (x, y) in positions:
        res = max(res, min( abs(x-a) + abs(y-b) for (a, b) in destinations ))
    return res

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

        #print(str(dist) + "     " + str(res))
        #print(print_board(board, state))

        Visited.add(frozenset(state))
        for move in dict_positions:
            # if move != opposite(res[-1]): # not always true in optimal path
            new_state = calculate_pos(state, move)
            if new_state not in Visited:
                new_dist = heura(new_state)
                if new_dist == 0:
                    return res[1:] + move

                Q.put((len(res) + new_dist, len(res), new_state, res + move))
                Visited.add(frozenset(new_state))
    return ""

def solve():
    positions = create_data()
    #print(pretty_print(dists))
    res = BFS(positions)
    #analise(positions, res)
    return res #+ " " + str(len(res))

if __name__ == '__main__':
    input = open('zad_input.txt').readlines()
    board = [line for line in input]

    with open('zad_output.txt', mode='w') as out_file:
        out_file.write(solve())