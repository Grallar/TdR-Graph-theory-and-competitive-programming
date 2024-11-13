#include<iostream>
#include<fstream>
#include<bits/stdc++.h>
using namespace std;

void bfs(int i, int j, int n, int m, vector<vector<char>>& my_map) {
	// input: alcada i, amplada j, alcada n, amplada m, matriu amb els # i .
	// fes una cua de parells de valors (seran indexos)
	queue<pair<int,int>>q; 
	/* Fes una llista amb els 4 valors donats, per a comprovar les caselles
	amunt, avall, a la dreta i l'esquerra de l'explorada */
	vector<int> moves = {1,-1,0,0}; 
	
	// Afegeix el parell i, j a la qua
	q.push({i,j}); 
	// Marca la casella corresponent a i, j com a #
	my_map[i][j] = '#';

	// Mentre la qua no estigui buida
	while (!q.empty()) {
		// Pren el primer parell de la cua i elimina'l
		int y = q.front().first;
		int x = q.front().second;
		q.pop();

		/* 4 vegades, comprova cada casella a l'esquerra, dreta, a sobre i a
		sota de l'actual.*/
		for (int k=0; k<4; k++) {
			int r = y + moves[k];
			int c = x + moves[3-k];

			// Si es una casella d'indexos valids i es terra
			if (c>=0 && r>=0 && c<m && r<n && my_map[r][c] == '.') {
				// Marca-la com a # i afegeix-la a la cua
				my_map[r][c] = '#';
				q.push({r,c});
			}
		}
	}
}

int main() {
	// Crea dues variables n, m, enters, i introdueix-hi les dades d'entrada
	int n, m; cin >> n >> m;

	// Crea una llista de llistes de caracters, la matriu
	vector<vector<char>> my_map(n, vector<char>(m));
	// Per a cada linia d'input
	for (int i = 0; i < n; i++) {
		// Per a cada caracter de la linia
		for (int j = 0; j < m; j++) {
			// Afegeix-lo a la casella corresponent
			cin >> my_map[i][j];
		}
	}

	// Crea una variable per al nombre d'habitacions
	int rooms = 0;
	// Per cada llista en la matriu del mapa
	for (int i = 0; i < n; i++) {
		// Per cada casella en cadascuna d'aquestes llistes
		for (int j = 0; j < m; j++) {
			// Si la casella es terra, afegeix una habitacio i explora-ho
			if (my_map[i][j] == '.') {
				rooms++;
				bfs(i,j,n,m,my_map);
			}
		}
	}
	// Imprimeix el nombre d'habitacions per la terminal.
	cout << rooms << endl;
}