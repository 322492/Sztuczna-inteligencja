from queue import Queue
import random
import copy

board = []
dict_positions = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
dict_positions_opposites = {'R': 'L', 'D': 'U', 'L': 'R', 'U': 'D'}

def print_board(brd, positions):
    b = ""
    for i in range(len(brd)):
        line = ""
        for j in range(len(brd[i])):
            if(board[i][j] == '#'):
                line += "#"
            elif((i, j) in positions):
                line += 'S'
            else:
                line += ' '
        b+= line + "\n"

    print(b)
                
def find_last_way(positions, destinations):
    s = list(positions)[0]

    if(s in destinations):
        return ""

    Q = Queue()
    Q.put((s, ""))
    Visited = set()

    while(not Q.empty()):
        ruch, r = Q.get()

        Visited.add(ruch)
        for d in dict_positions:
            next_move = (ruch[0] + dict_positions[d][0], ruch[1] + dict_positions[d][1])
            if(next_move in destinations):
                return r + d
            if(board[next_move[0]][next_move[1]] != '#'):
                if(next_move in destinations):
                    return r + d
                if(next_move not in Visited):
                    Q.put((next_move, r + d))
                    Visited.add(next_move)
    return r

def count_pos(positions, direction):
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
    return dict_positions_opposites[x]

def try_maximum_reduce(positions, res):
    word = "ULDR"
    last_one = random.choice(word)

    while(len(res) <= 150 and len(positions) > 1):
        curr_one = random.choice(word)
        while(curr_one == opposite(last_one)):
            curr_one = random.choice(word)
        new_pos = count_pos(positions, curr_one)
        positions = new_pos
        res += curr_one
        last_one = curr_one

    return positions, res

def analise(positions, res):
    brd = copy.deepcopy(board)
    print_board(brd, positions)
    for c in res:
        print(c)
        positions = count_pos(positions, c)
        print_board(brd, positions)

def solve(board):
    positions = set()
    destinations = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'S':
                positions.add((i, j))
            if board[i][j] == 'B':
                destinations.add((i, j))
                positions.add((i, j))
            if board[i][j] == 'G':
                destinations.add((i, j))
    
    while(True):
        res = ""
        position, res = try_maximum_reduce(positions, res)
        if(len(res) > 150):
            continue
        else:
           # print('AAAAAANALIZA')
           # analise(positions, res)
            res += find_last_way(position, destinations)
            if(len(res) > 150):
                continue
            else:
                break
    return res

if __name__ == '__main__':
    input = open('zad_input.txt').readlines()
    board = [line for line in input]

    with open('zad_output.txt', mode='w') as out_file:
        out_file.write(solve(board))