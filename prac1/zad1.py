import sys
import math
from queue import Queue

def on_board(pos): # p = proponowana pozycja figury
    plist = list(pos)
    if plist[0] < 'a' or plist[0] > 'h' or plist[1] < '1' or plist[1] > '8':
        return False
    return True

def possible(ruch, p): # p = proponowana pozycja figury
    if not on_board(p) or p == ruch[1] or p == ruch[2] or p == ruch[3]:
        return False
    return True

#zmienianie znaku w stringu, word - słowo, w którym zmienię znak, which - pozycja zmienianego znaku, how - o ile w tablicy ascii zmieniam znak
def char_set(word, which, how):
    wlist = list(word)
    wlist[which] = chr(ord(wlist[which]) + how)
    word = "".join(wlist)
    return word

def szach(ruch, pos): # czy czarny jest szachowany
    wk = ruch[1]
    ww = ruch[2]

    if(ww != pos):
        for i in (0, 1):
            if(ww[i] == pos[i] and (wk[i] != pos[i] or wk==pos)):
                return True

    if(wk != pos):
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                nww = wk
                nww = char_set(nww, 0, i)
                nww = char_set(nww, 1, j)
                if nww == pos:
                    return True
    return False

# czy biały jest szachowany (służy do wykluczania niedozwolonych ruchów)
def szach_czarnych(ruch, pos):
    czarny = ruch[3]

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            nww = czarny
            nww = char_set(nww, 0, i)
            nww = char_set(nww, 1, j)
            if nww == pos:
                return True
    return False
    
def czy_mat(ruch):

    if(ruch[0] == "white"):
        return False

    if not szach(ruch, ruch[3]):
        return False

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            pos = ruch[3]
            pos = char_set(pos, 0, i)
            pos = char_set(pos, 1, j)
            if on_board(pos) and not szach(ruch, pos):
                return False
            
    return True

def find_mat(first_move, Dict):

    Q = Queue() #kolejka do BFS
    Q.put(first_move)
    Visited = set()

    while(True):
        ruch = Q.get() # Remove and return an item from the queue.

        if ruch in Visited:
            continue

        Visited.add(ruch)

        if(czy_mat(ruch)):
            return ruch

        if ruch[0] == "black":
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    npos = ruch[3]
                    npos = char_set(npos, 0, i)
                    npos = char_set(npos, 1, j)
                    next = list(ruch)
                    next[0] = "white"
                    next[3] = npos
                    if possible(ruch, next[3]) and tuple(next) not in Visited and not szach(ruch, next[3]):
                        Dict[tuple(next)] = ruch
                        Q.put(tuple(next))

        if ruch[0] == "white":
            #opcje króla
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    npos = ruch[1]
                    npos = char_set(npos, 0, i)
                    npos = char_set(npos, 1, j)
                    next = list(ruch)
                    next[0] = "black"
                    next[1] = npos
                    if possible(ruch, next[1]) and tuple(next) not in Visited and not szach_czarnych(ruch, next[1]):
                        Dict[tuple(next)] = ruch
                        Q.put(tuple(next))

            #opcje wieży
            for i in range(-8, 9):
                npos = ruch[2]
                npos = char_set(npos, 0, i)
                next = list(ruch)
                next[0] = "black"
                next[2] = npos
                if possible(ruch, next[2]) and tuple(next) not in Visited and not szach_czarnych(ruch, next[1]):
                    Dict[tuple(next)] = ruch
                    Q.put(tuple(next))
            for i in range(-8, 9):
                npos = ruch[2]
                npos = char_set(npos, 1, i)
                next = list(ruch)
                next[0] = "black"
                next[2] = npos
                if possible(ruch, next[2]) and tuple(next) not in Visited and not szach_czarnych(ruch, next[1]):
                    Dict[tuple(next)] = ruch
                    Q.put(tuple(next))

def difference(next, prev):
    for i in (1, 2, 3):
        if next[i] != prev[i]:
            return prev[i] + next[i]

def solve(first_move, debug = False):
    Dict = {} # słownik do odzyskiwania ścieżki (key, value) = (ruch aktualny, ruch poprzedni)
    Dict[first_move] = "END"
    ruch = find_mat(first_move, Dict)

    #print(ruch) # pozycja mata

    res = []
    while(Dict[ruch] != "END"):
        res.append(difference(ruch, Dict[ruch]))
        ruch = Dict[ruch]

    res.reverse()

    if not debug:
        return len(res)

    return " ".join(res)

if __name__ == '__main__':
    with open('zad1_input.txt', mode='r') as in_file, open('zad1_output.txt', mode='w') as out_file:
        for line in in_file:
            moving_player, white_king, white_rook, black_king = line.split(" ")
            pierwszy_ruch = (moving_player, white_king, white_rook, black_king)
            out_file.write(f'{solve(pierwszy_ruch)}\n')