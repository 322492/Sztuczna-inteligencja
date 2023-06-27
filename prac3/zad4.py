
def B(i,j):
    return 'B_%d_%d' % (i,j)
    
def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')
    
    R = len(rows)
    C = len(cols)
    
    bs = [ B(i,j) for i in range(R) for j in range(C)]
    
    writeln('solve([' + ', '.join(bs) + ']) :- ')
    
    # domain in 0..1
    writeln('[' + ', '.join(bs) + '] ins 0..1,')

    # sums in rows
    for i, sum in enumerate(rows):
        x = [B(i, j) for j in range(C)]
        writeln('sum([' + ', '.join(x) + '], #=, ' + str(sum) + '), ')

    # sums in columns
    for j, sum in enumerate(cols):
        x = [B(i, j) for i in range(R)]
        writeln('sum([' + ', '.join(x) + '], #=, ' + str(sum) + '), ')

    # declarations
    for x, y, v in triples:
        output.write('%s #= %d, ' % (B(x, y), v))

    # b = 1 => a + c > 0 for rows
    for i in range(R):
        for j in range(C - 2):
            a = B(i, j)
            b = B(i, j + 1)
            c = B(i, j + 2)
            writeln(b + ' #= 1 #==> ' + a + ' + ' + c + ' #>= 1, ')

    # B = 1 => A + C > 0 for columns
    for i in range(C):
        for j in range(R - 2):
            a = B(i, j)
            b = B(i, j + 1)
            c = B(i, j + 2)
            writeln(b + ' #= 1 #==> ' + a + ' + ' + c + ' #>= 1, ')

    # a + d = 2 <=> b + c = 2
    for i in range(R - 1):
        for j in range(C - 1):
            a = B(i, j)
            b = B(i, j + 1)
            c = B(i + 1, j)
            d = B(i + 1, j + 1)
            writeln(a + ' + ' + d + ' #= 2 #<==> ' + b + ' + ' + c + ' #= 2, ')

    writeln('')
    writeln('    labeling([ff], [' +  ', '.join(bs) + ']).' )
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")

def writeln(s):
    output.write(s + '\n')

txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(map(int, txt[i].split()))

storms(rows, cols, triples)            
        

