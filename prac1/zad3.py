'''
karta to para (n, k), gdzie 1 < n < 15 to figura (W = 11, D = 12, K = 13 i A = 14), zaś k to kolor (pik, kier, karo, trefl)
reka to 5 kart
'''

import random

def poker(reka):
    reka.sort()
    for i in range(0, 4):
        if reka[i][0] + 1!= reka[i + 1][0] or reka[i][1] != reka[i+1][1]:
            return False
    return True

def kareta(reka):
    reka.sort()
    if reka[0][0] == reka[1][0] == reka[2][0] == reka[3][0]:
        return True
    if reka[1][0] == reka[2][0] == reka[3][0] == reka[4][0]:
        return True
    return False

def full(reka):
    reka.sort()
    if reka[0][0] == reka[1][0] == reka[2][0] and reka[3][0] == reka[4][0]:
        return True
    if reka[0][0] == reka[1][0] and reka[2][0] == reka[3][0] == reka[4][0]:
        return True
    return False

def kolor(reka):
    for i in range(0, 4):
        if reka[i][1] != reka[i + 1][1]:
            return False
    return True

def strit(reka):
    reka.sort()
    for i in range(0, 4):
        if reka[i][0] + 1 != reka[i + 1][0]:
            return False
    return True

def trojka(reka):
    reka.sort()
    for i in range(0, 3):
        if reka[i][0] == reka[i + 1][0] == reka[i + 2][0]:
            return True
    return False

def dwie_pary(reka):
    reka.sort()
    if reka[0][0] == reka[1][0] and reka[2][0] == reka[3][0]:
        return True
    if reka[0][0] == reka[1][0] and reka[3][0] == reka[4][0]:
        return True
    if reka[1][0] == reka[2][0] and reka[3][0] == reka[4][0]:
        return True
    return False

def para(reka):
    reka.sort()
    for i in range(0, 4):
        if reka[i][0] == reka[i + 1][0]:
            return True
    return False

#zwraca wartość punktową dla pięcioelementowej ręki [poker, kareta(4), full(3+2), kolor, strit, trójka, dwie pary, para, wysoka karta] = [10, 9, 8, 7, 6, 5, 4, 3, 2]
def uklad(reka):
    if poker(reka):
        return 10
    if kareta(reka):
        return 9
    if full(reka):
        return 8
    if kolor(reka):
        return 7
    if strit(reka):
        return 6
    if trojka(reka):
        return 5
    if dwie_pary(reka):
        return 4
    if para(reka):
        return 3
    return 0

# zwraca 1 jeśli wygrywa Blotkarz i 0 wpp
def test(Figurant, Blotkarz):
    rekaF = random.sample(Figurant, 5)
    rekaB = random.sample(Blotkarz, 5)

    if(uklad(rekaB) > uklad(rekaF)):
        return 1
    return 0

def standard_talie():
    TaliaF = [11, 12, 13, 14]
    Figurant = [(i, j) for i in TaliaF for j in range(1, 5)]

    TaliaB = range(2, 11)
    Blotkarz = [(i, j) for i in TaliaB for j in range(1, 5)]

    return Figurant, Blotkarz

# n = liczba testów
def staty(n, TaliaF, TaliaB):
    wygranaB = 0
    for _ in range(n):
        wygranaB += test(TaliaF, TaliaB)

    return wygranaB / n * 100, n

F, B = standard_talie()
p, n = staty(100000, F, B)
print(f"Blotkarz ma około {p}% szans na wygraną przy {n} grach przy taliach opisanych w zadanu.")

# optymalne talie Blotkarza
def check_options():
    TaliaF = [11, 12, 13, 14]
    Figurant = [(i, j) for i in TaliaF for j in range(1, 5)]

    TaliaB = range(2, 5) # tylko trzy figury
    Blotkarz = [(i, j) for i in TaliaB for j in range(1, 5)]

    n = 100000

    p, n = staty(n, Figurant, Blotkarz)

    if(p > 50):
        print(f"Statystycznie Blotkarz wygrywa z prawdopodobieństwiem około {p}% w {n} grach i talią:")
        print(Blotkarz)
        print(f"o długości {len(Blotkarz)}.\nNie udało mi się zwiększyć liczby kart w talii przy zachowaniu takiego wyniku.")
    return

check_options()

