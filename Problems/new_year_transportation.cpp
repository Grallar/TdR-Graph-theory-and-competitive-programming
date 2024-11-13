#include <bits/stdc++.h>
using namespace std;

bool dfs(vector<vector<int>>& adj, int i, int t) {
    if (i == t) return true; // Si s'arriba al vertex buscat, retorna true

    // Per a cada vertex en la llista d'adjacencia.
    for (int j = 0; j < adj[i].size(); j++) { 
        if (dfs(adj,adj[i][j],t)) return true; // Si la funcio dfs retorna true, retorna true.
    }

    return false; // Retorna false (s'arriba aqui en cas que no hi hagi cami)

}

int main() {
    int n, t; // Crea dos variables per a enters
    cin >> n >> t; // introdueix a ambdues variables els valors d'entrada

    vector<vector<int>> adj(n+1); // Crea una llista de llistes d'enters
    for (int i = 1; i < n; i++) { // Per a cada vertex 
        int a_i; cin >> a_i; // Guarda a la variable a_i el valor introduit
    // Guarda a la llista d'adjacencia, per al vertex i, la suma del vertex 
    // i d'a_i
    adj[i].push_back(i + a_i); 
    }
    // Si la funcio dfs retorna true, imprimeix YES per la terminal
    if (dfs(adj,1,t)) cout << "YES\n"; 
    // Sino, imprimeix NO per la terminal
    else cout << "NO\n";
}