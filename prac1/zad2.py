def make_dictionary():
    words = open('polish_words.txt', 'r')
    dict = set()
    length_of_longest_word = 0
    for line in words:
        dict.add(line[:-1])
        length_of_longest_word = max(length_of_longest_word, len(line))
    return dict, length_of_longest_word

def my_split(Dict, length_of_longest_word, line):
    line = '#' + line[:-1] #inicjalizacja # wyrazu pustego na początku i usuniecie znaku nowej linii
    n = len(line)
    dp = [1] + [0] * (n + length_of_longest_word) # dp[i] = maksymalna suma kwadratów, którą jestem w stanie uzyskać z podsłowa o długości i
    dp2 = [-1] * (n + length_of_longest_word + 1) # dp2[i] = długość słowa, które kończy optymalne rozbicie podsłowa długości i 

    for i in range(0, n):
        if dp[i] > 0:
            for j in range(1, length_of_longest_word + 1):
                if i + j + 1 > n:
                    break
                s = line[i + 1 : i + j + 1]
                if s in Dict:
                    if dp[i + j] < dp[i] + j*j:
                        dp[i + j] = dp[i] + j*j
                        dp2[i + j] = j

    res = ""
    i = n - 1
    j = dp2[i]

    # odzyskiwanie wyniku, na razie słów w odwrotnej kolejności
    while i > 0:
        #print(f"{i, j}")
        res += line[i - j + 1:i + 1] + " "
        i -= j
        j = dp2[i]

    res = "".join(w + " " for w in res.split()[::-1]) # odrócenie kolejności słów w res
    #print(res)
    return res

if __name__ == '__main__':
    Dict, length_of_longest_word = make_dictionary()
    with open('zad2_input.txt', mode='r') as in_file, open('zad2_output.txt', mode='w') as out_file:
        for line in in_file:
            out_file.write(f'{my_split(Dict, length_of_longest_word, line)}\n')
