from queue import Queue

dict_positions = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
destinations = set()
board = ["" for _ in range(20)]
n = 0
m = 0

def pretty_print(player, boxes, result):
    print(result)
    res = ""
    for (bx, by) in boxes:
        res += (f"({bx}, {by}) ")
    res += '\n'
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (i, j) == player:
                res += 'K'
            elif (i, j) in destinations and (i, j) in boxes:
                res += '*'
            elif (i, j) == player and (i, j) in destinations:
                res += '+'
            elif (i, j) in boxes:
                res += 'B'
            elif (i, j) in destinations:
                res += 'G'
            elif board[i][j] == 'W':
                res += board[i][j]
            else:
                res += '.'
        if res[-1] != '\n':
            res += '\n'
    print(res)

def print_boxes(boxes):
    res = ""
    for (bx, by) in boxes:
        res += (f"({bx}, {by}) ")
    print(res)

def in_the_corner(bx, by):
    if board[bx + 1][by] == 'W' and board[bx][by + 1] == 'W': # DR
        return True
    if board[bx][by + 1] == 'W' and board[bx - 1][by] == 'W': # RU
        return True
    if board[bx - 1][by] == 'W' and board[bx][by - 1] == 'W': # UL
        return True
    if board[bx][by - 1] == 'W' and board[bx + 1][by] == 'W': # LD
        return True
    return False

def no_parallel_dest(d):
    if(d == 'R'):
        for (x, y) in destinations:
            if y == m - 1:
                return False
    if(d == 'D'):
        for (x, y) in destinations:
            if x == n - 1:
                return False
    if(d == 'L'):
        for (x, y) in destinations:
            if y == 1:
                return False
    if(d == 'U'):
        for (x, y) in destinations:
            if x == 1:
                return False
    return True

def one_more_thing(bx, by):
    if bx == n - 1 and no_parallel_dest('D'):
        return True
    if by == m - 1 and no_parallel_dest('R'):
        return True
    if by == 1 and no_parallel_dest('L'):
        return True
    if bx == 1 and no_parallel_dest('U'):
        return True
    
def reasonable(boxes):
    for (bx, by) in boxes:
        if (bx, by) not in destinations:
            if in_the_corner(bx, by): # box is in the corner
                return False
            if one_more_thing(bx, by): # box is next to wall and there is no destination near that wall = you have to push box from the wall but it is impossible
                return False
    return True

def solve(input_board):
    n = len(input_board)
    m = len(input_board[0])
    start_player = (0, 0)
    start_boxes = set()

    for i in range(len(input_board)):
        for j in range(len(input_board[i])):
            if input_board[i][j] == 'B':
                start_boxes.add((i, j))
                board[i] += '.'
            if input_board[i][j] == 'G':
                destinations.add((i, j))
                board[i] += '.'
            if input_board[i][j] == '*':
                start_boxes.add((i, j))
                destinations.add((i, j))
                board[i] += '.'
            if input_board[i][j] == 'K':
                start_player = (i, j)
                board[i] += '.'
            if input_board[i][j] == '+':
                start_player = (i, j)
                destinations.add((i, j))
                board[i] += '.'
            if input_board[i][j] == 'W':
                board[i] += 'W'
            if input_board[i][j] == '.':
                board[i] += '.'

    Q = Queue() # state = (player, set of boxes positions, result)
    vis = set()
    Q.put((start_player, start_boxes, ""))

    while not Q.empty():
        (player, boxes, result) = Q.get()
        #pretty_print(player, boxes, result)

        vis.add((player, frozenset(boxes)))
        for d in dict_positions:
            (nx, ny) = (player[0] + dict_positions[d][0], player[1] + dict_positions[d][1])
            if board[nx][ny] != 'W':
                if (nx, ny) in boxes: # want to move box
                    nbx = nx + dict_positions[d][0]
                    nby = ny + dict_positions[d][1]
                    if (nbx, nby) not in boxes and board[nx + dict_positions[d][0]][ny + dict_positions[d][1]] != 'W': # we can move the box
                        boxes.remove((nx, ny))
                        boxes.add((nbx, nby))
                        if((nx, ny), frozenset(boxes)) not in vis and reasonable(boxes):
                            Q.put(((nx, ny), boxes.copy(), result + d))
                            if(boxes == destinations):
                                return result + d
                            vis.add(((nx, ny), frozenset(boxes)))

                        boxes.remove((nbx, nby))
                        boxes.add((nx, ny))
                if (nx, ny) not in boxes:
                    if((nx, ny), frozenset(boxes)) not in vis and reasonable(boxes):
                        Q.put(((nx, ny), boxes.copy(), result + d))
                        vis.add(((nx, ny), frozenset(boxes)))

    return "XD"

if __name__ == '__main__':
    input = open('zad_input.txt').readlines()
    input_board = [line for line in input]

    with open('zad_output.txt', mode='w') as out_file:
        out_file.write(solve(input_board))