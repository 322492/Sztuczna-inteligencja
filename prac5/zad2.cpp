#include <bits/stdc++.h>

using namespace std;

// packing maximum square in first free space

string X = ".ABCDEFGHIJKLMNOPQRSTUVWX";
const int n = 70;
int A[n][n] = {0};

void answer()
{
    int sum = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (A[i][j] == 0)
                sum++;

    cout << sum << "\n";
    cout << "    ";
    for (int i = 1; i <= n; i++)
        cout << i;
    cout << "\n";
    for (int i = 0; i < n; i++)
    {
        if (i + 1 < 10)
            cout << i + 1 << ":  ";
        else
            cout << i + 1 << ": ";
        for (int j = 0; j < n; j++)
        {
            if (j + 1 < 10)
                cout << X[A[i][j]];
            else
                cout << X[A[i][j]] << " ";
        }
        cout << "\n";
    }
    return;
}

bool possible(int a, int b, int x)
{
    for (int i = a; i < a + x; i++)
        for (int j = b; j < b + x; j++)
            if (i >= n || j >= n || A[i][j] != 0)
                return false;

    return true;
}

void fill(int a, int b, int x)
{
    for (int i = a; i < a + x; i++)
        for (int j = b; j < b + x; j++)
            A[i][j] = x;
    return;
}

int main()
{
    int w = 24;
    while (w > 0)
    {
        bool filled = false;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (possible(i, j, w))
                {
                    fill(i, j, w);
                    w--;
                    filled = true;
                    break;
                }
            }
            if (filled)
                break;
        }
        if (!filled)
            w--;
    }

    answer();

    return 0;
}