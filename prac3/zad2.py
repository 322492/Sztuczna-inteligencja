from queue import Queue

def column(i):
    return [row[i] for row in board]

def gen_all(lst, n):
    res = []
    white = -1 # deciding if white block are 0s or -1s or something else

    if n == 0:
        return [[]]
    if len(lst) == 0:
        return [[white] * n]

    # add white
    if sum(lst) + len(lst) - 1 < n:
        res += [[white] + r for r in gen_all(lst, n - 1)]

    # add block of 1s
    ones = [1 for _ in range(lst[0])]
    new_n = n - lst[0]

    if len(lst) > 1:
        ones += [white]
        new_n -= 1

    res += [ones + rest for rest in gen_all(lst[1:], new_n)]

    return res

def pretty_print():
    res = ""
    for i in range(0, n):
        for j in range(0, m):
            if board[i][j] == 1:
                res += '#'
            elif board[i][j] == 0:
                res += '-'
            else:
                res += '.'
        res += "\n"

    return res

def deduce_row(r):
    poss = all_poss_rows[r]
    if len(poss) == 0: # there is no possibilities to solution - I guessed something wrong and need to backtrack
        return False
    better_poss = poss.copy()
    row = board[r]

    for i in range(m):
        if row[i] != 0:
            for j in range(len(poss)):
                if poss[j][i] != row[i] and poss[j] in better_poss:
                    better_poss.remove(poss[j])

    poss = better_poss
    if len(poss) == 0: # there is no possibilities to solution - I guessed something wrong and need to backtrack
        return False
    all_poss_rows[r] = poss

    for i in range(m):
        s = 0
        sm = 0
        for p in poss:
            if p[i] == 1:
                s += 1
            if p[i] == -1:
                sm += -1
        if s == len(poss) and board[r][i] == 0:  # has to be black
            board[r][i] = 1
            Q.put((i, -1))
        if -sm == len(poss) and board[r][i] == 0:  # it has to be white
            board[r][i] = -1
            Q.put((i, -1))

    return True

def deduce_column(c):
    poss = all_poss_cols[c]
    if len(poss) == 0: # there is no possibilities to solution - I guessed something wrong and need to backtrack
        return False
    better_poss = poss.copy()
    col = column(c)

    for i in range(n):
        if col[i] != 0:
            for j in range(len(poss)):
                if poss[j][i] != col[i] and poss[j] in better_poss:
                    better_poss.remove(poss[j])

    poss = better_poss
    if len(poss) == 0: # there is no possibilities to solution - I guessed something wrong and need to backtrack
        return False
    all_poss_cols[c] = poss

    for i in range(n):
        s = 0
        sm = 0
        for p in poss:
            if p[i] == 1:
                s += 1
            if p[i] == -1:
                sm += -1
        if s == len(poss) and board[i][c] == 0:  # has to be black
            board[i][c] = 1
            Q.put((-1, i))
        if -sm == len(poss) and board[i][c] == 0:  # it has to be white
            board[i][c] = -1
            Q.put((-1, i))
                        
    return True

def just_do_it(i, j):
    if i == -1:
        return deduce_row(j)
    if j == -1:
        return deduce_column(i)

def ready(board):
    for i in range(n):
        if 0 in board[i]:
            return False
    return True

def guess():
    global board, all_poss_rows, all_poss_cols
    old_board = [x[:] for x in board]
    old_all_poss_rows = [x[:] for x in all_poss_rows]
    old_all_poss_cols = [x[:] for x in all_poss_cols]

    position_to_change = (0, 0)
    found = False
    for i in range(n):
        for j in range(m):
            if board[i][j] == 0:
                position_to_change = (i, j)
                found = True
                break
        if found:
            break

    change_to = 1

    board[position_to_change[0]][position_to_change[1]] = change_to
    Q.put((-1, position_to_change[0]))
    Q.put((position_to_change[1], -1))
    solved = solve()
    if solved:
        with open('zad_output.txt', mode='w') as out_file:
            out_file.write(pretty_print())
    else:
        board = old_board
        all_poss_rows = old_all_poss_rows
        all_poss_cols = old_all_poss_cols
        board[position_to_change[0]][position_to_change[1]] = -change_to
        Q.put((-1, position_to_change[0]))
        Q.put((position_to_change[1], -1))
        solved = solve()

def solve():
    while True:
        if not Q.empty():
            (i, j) = Q.get()
            everything_good = just_do_it(i, j)
            if not everything_good: # I guessed something wrong and need to backtrack
                return False 
        elif ready(board):
            return True # I found solution
        else: # I have to choose random
            guess()

if __name__ == '__main__':
    input = open('zad_input.txt').readlines()
    global n, m # n rows and m columns -> row has m fields, column has n fields
    n, m = [int(x) for x in input[0].split()]
    rAndK = [[int(x) for x in line.split()] for line in input[1:]]
    global rows, columns
    rows = rAndK[:n]
    columns = rAndK[n:]

    global board, all_poss_rows, all_poss_cols
    board = [[0] * m for _ in range(n)]
    all_poss_rows = [gen_all(lst, m) for lst in rows]
    all_poss_cols = [gen_all(lst, n) for lst in columns]

    global Q
    Q = Queue()  # rows and column to deducing
    # ith row = (-1, i), jth column = (j, -1)
    for i in range(n):
        Q.put((-1, i))

    for i in range(m):
        Q.put((i, -1))

    solved = solve()
    if solved:
        with open('zad_output.txt', mode='w') as out_file:
            out_file.write(pretty_print())