def opt_dist(lst, D):

    inner = lst[0:D].count('1') #liczba jedynek w rozpatrywanym przedziale
    outer = lst.count('1') - inner #liczba jedynek poza przedziałem

    a = 0
    b = D - 1

    res = D - inner + outer
    a += 1
    b += 1

    while b < len(lst):
        if lst[a-1] == '1':
            inner -= 1
            outer += 1
        if lst[b] == '1':
            inner += 1
            outer -= 1
        res = min(res, D - inner + outer) #D-inner to liczba zer w rozważanym przedziale do zamiany, a outer liczba jedynek do zamiany poza przedziałem
        #print(f"", a, " ", b, lst[a:b+1], " ", inner, " ", outer)
        a += 1
        b += 1

    return res

if __name__ == '__main__':
    with open('zad4_input.txt', mode='r') as in_file, open('zad4_output.txt', mode='w') as out_file:
        for line in in_file:
            bits, D = line.split(" ")
            out_file.write(f'{opt_dist(bits, int(D))}\n')
