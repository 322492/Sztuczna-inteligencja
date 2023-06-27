#include <bits/stdc++.h>

using namespace std;

// struct mt
// {
//     int amount; // amoubnt of resources
//     int cell;   // index of cell
// };

struct eth
{
    int type;     // 0 - nothing, 1 - eggs, 2 - crystals
    int amount;   // amount of resources (type = 0 -> amount = 0)
    int my_ants;  // the amount of your ants on this cell
    int opp_ants; // the amount of opponent ants on this cell
};

int n; // amount of hexagonal cells in this map
int number_of_bases;
int my_base;
vector<vector<int>> area; // area graph
vector<int> dist;         // dist[i] = distance from nearest base
vector<int> bases;        // my bases
vector<int> opponents;    // opponents bases
vector<eth> cells;        // cells[i] = some info about cell i
vector<int> visited;      // auxiliary in BFS
// vector<mt> crystals;
// vector<mt> eggs;

void BFS()
{
    // creating vector dist long enough
    for (int i = 0; i < n; i++)
    {
        dist.push_back(0);
        visited.push_back(false);
    }

    queue<int> Q;
    int v;
    Q.push(my_base);

    while (!Q.empty())
    {
        v = Q.front();
        Q.pop();
        visited[v] = true;

        for (int i : area[v])
            if (visited[i] == false)
            {
                dist[i] = dist[v] + 1;
                visited[i] = true;
                Q.push(i);
            }
    }
    return;
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    cin >> n;
    cin.ignore();

    int type;                                                 // 0 for empty, 1 for eggs, 2 for crystal
    int initial_resources;                                    // the initial amount of eggs/crystals on this cell
    int neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5; // the index of the neighbouring cell for each direction
    for (int i = 0; i < n; i++)
    {
        cin >> type >> initial_resources >> neigh_0 >> neigh_1 >> neigh_2 >> neigh_3 >> neigh_4 >> neigh_5;
        cin.ignore();

        cells.push_back({type, initial_resources, 0, 0});

        vector<int> neigh;
        if (neigh_0 != -1)
            neigh.push_back(neigh_0);
        if (neigh_1 != -1)
            neigh.push_back(neigh_1);
        if (neigh_2 != -1)
            neigh.push_back(neigh_2);
        if (neigh_3 != -1)
            neigh.push_back(neigh_3);
        if (neigh_4 != -1)
            neigh.push_back(neigh_4);
        if (neigh_5 != -1)
            neigh.push_back(neigh_5);
        area.push_back(neigh);

        //  mt c = {initial_resources, i};
        ///  if (type == 1)
        //      eggs.push_back(c);
        //  if (type == 2)
        //      crystals.push_back(c);
    }

    int my_base_index;
    cin >> number_of_bases;
    cin.ignore();
    for (int i = 0; i < number_of_bases; i++)
    {
        cin >> my_base_index;
        cin.ignore();
        bases.push_back(my_base_index);
        my_base = my_base_index;
    }
    for (int i = 0; i < number_of_bases; i++)
    {
        int opp_base_index;
        cin >> opp_base_index;
        cin.ignore();
        opponents.push_back(opp_base_index);
    }

    BFS();

    // game loop
    while (1)
    {
        vector<int> do_line;
        int sum = 0;
        for (int i = 0; i < n; i++)
        {
            int resources; // the current amount of eggs/crystals on this cell
            int my_ants;   // the amount of your ants on this cell
            int opp_ants;  // the amount of opponent ants on this cell

            cin >> resources >> my_ants >> opp_ants;
            cin.ignore();

            cells[i].amount = resources;
            cells[i].my_ants = my_ants;
            cells[i].opp_ants = opp_ants;

            // I want to harvest nearby resources as fast as possible
            if (cells[i].type == 1 && resources > 0 && dist[i] <= 2)
                do_line.push_back(i);

            sum += resources;
        }

        for (auto i : do_line)
            cout << "LINE " << i << " " << my_base << " " << 1 << ";"; // TODO: better lines - the farthest field the more beacons

        if (do_line.size() == 0)
        {
            // vector<triple> rest;
            // TODO: not really to all of them because I cannot reach them (I have to small amount of ant) so calculate closest and reachable
            // TODO: not go for aggs when they'ra far away and in the end of game
            // TODO: if the resources are the same size then go for nearer
            for (int i = 0; i < n; i++)
            {
                if (cells[i].amount > 0)
                {
                    cout << "LINE " << i << " " << my_base << " " << (int)((cells[i].amount * 1000)/sum + 1) << ";";
                }
            }
        }
        cout << endl;

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;

        // WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
        // cout << "WAIT" << endl;
    }
}