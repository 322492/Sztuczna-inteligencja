import random

def opt_dist(lst, D):

    inner = lst[0:D].count(1) #liczba jedynek w rozpatrywanym przedziale
    outer = lst.count(1) - inner #liczba jedynek poza przedziałem

    (a, b) = (0, D - 1)

    res = D - inner + outer
    (a, b) = (a + 1, b + 1)

    while b < len(lst):
        if lst[a-1] == 1:
            (inner, outer) = (inner - 1, outer + 1)
        if lst[b] == 1:
            (inner, outer) = (inner + 1, outer - 1)
        res = min(res, D - inner + outer) #D-inner to liczba zer w rozważanym przedziale do zamiany, a outer liczba jedynek do zamiany poza przedziałem
        (a, b) = (a + 1, b + 1)

    return res

def column(arr, i):
    return [row[i] for row in arr]

def finished(board, n, m, rows, columns):

    for i in range(0, n):
        if opt_dist(board[i], rows[i]) != 0:
            return False

    for j in range(0, m):
        if opt_dist(column(board, j), columns[j]) != 0:
            return False

    return True

def all_rows_perfect(board, n, rows):
    for i in range(0, n-1):
        if opt_dist(board[i], rows[i]) != 0:
            return False
    return True

def all_columns_perfect(board, m, columns):
    for j in range(0, m-1):
        if opt_dist(column(board, j), columns[j]) != 0:
            return False
    return True

def change_a_row(board, n, m, rows, columns):

    #searching bad row
    i = random.randint(0, n-1)
    row_to_change = board[i]
    while opt_dist(row_to_change, rows[i]) == 0:
        i = random.randint(0, n-1)
        row_to_change = board[i]

    #searching for best j in i'th row
    best_change = n + m
    best_j = 0

    for j in range(0, m):
        board[i][j] = (board[i][j] + 1) % 2
        curr_change = opt_dist(board[i], rows[i]) + opt_dist(column(board, j), columns[j])
        if curr_change < best_change:
            best_change = curr_change
            best_j = j
        board[i][j] = (board[i][j] + 1) % 2

    board[i][best_j] = (board[i][best_j] + 1) % 2
    return board

def change_a_column(board, n, m, rows, columns):

    #searching bad column
    j = random.randint(0, m-1)
    column_to_change = column(board, j)
    while opt_dist(column_to_change, columns[j]) == 0:
        j = random.randint(0, m-1)
        column_to_change = column(board, j)

    #searching for best i in j'th column
    best_change = n + m
    best_i = 0

    for i in range(0, n):
        board[i][j] = (board[i][j] + 1) % 2
        curr_change = opt_dist(board[i], rows[i]) + opt_dist(column(board, j), columns[j])
        if curr_change < best_change:
            best_change = curr_change
            best_i = i
        board[i][j] = (board[i][j] + 1) % 2

    board[best_i][j] = (board[best_i][j] + 1) % 2
    return board

def change_something(board, n, m, rows, columns):
    co = random.randint(0, 1)

    if co == 0 and not all_rows_perfect(board, n, rows):
        return change_a_row(board, n, m, rows, columns)
    elif co == 1 and not all_columns_perfect(board, m, columns):
        return change_a_column(board, n, m, rows, columns)
    else:
        return board


def pretty_print(board, n, m):
    res = ""
    for i in range(0, n):
        for j in range(0, m):
            if board[i][j] == 1:
                res += '#'
            else:
                res += '.'
        res += "\n"

    return res

def solve(n, m, rows, columns):
    # board = [[0] * m] * n  # NEVER DO THIS AGAIN :(
    board = [[0]*m for _ in range(n)]

    zostalo_prob = 1000

    while zostalo_prob > 0:
        if not finished(board, n, m, rows, columns):
            board = change_something(board, n, m, rows, columns)
        else:
            return pretty_print(board, n, m)
        zostalo_prob -= 1

    return solve(n, m, rows, columns)

if __name__ == '__main__':
    input = open('zad5_input.txt').readlines()
    n, m = int(input[0][0]), int(input[0][2])
    rows = []
    columns = []

    for i in range(1, n + 1):
        rows.append(int(input[i]))
    for i in range(n + 1, n + m + 1):
        columns.append(int(input[i]))

    with open('zad5_output.txt', mode='w') as out_file:
        out_file.write(solve(n, m, rows, columns))