#include <iostream>
#include <bits/stdc++.h>

using namespace std;

#define ii pair<int, int> //
#define mp make_pair

int n, m;
int dx[4] = {1,0,-1,0};
int dy[4] = {0,1,0,-1};
string moves = "RDLU"; 


string getPath(vector<vector<int>>& prevStep, ii start, ii end) {
	auto [r,c] = end;
	string path = "";
	while (r != start.first || c != start.second) {
		int i = prevStep[r][c];
		path.push_back(moves[i]);
		r -= dy[i];
		c -= dx[i];
	}
	reverse(path.begin(), path.end());

	return path;
}



bool valid(vector<vector<char>>& maze, int r, int c) {
	if (r < 0 || r >= n || c < 0 || c >= m) return false;
	if (maze[r][c] == '#') return false;

	return true;
}


bool bfs(vector<vector<char>>& maze, vector<vector<int>>& prevStep, ii start, ii end) {	
	queue<ii> q;
	q.push(start);

	while (!q.empty()) {
		ii node = q.front();
		q.pop();

		for (int i = 0; i < 4; i++) {
			int new_r = node.first + dy[i];
			int new_c = node.second + dx[i]; 
	
			if (valid(maze, new_r, new_c)) {

				prevStep[new_r][new_c] = i;

				if (maze[new_r][new_c] == 'B') {	
					return true;
				} else {
					maze[new_r][new_c] = '#';
					ii node = mp(new_r, new_c);
					q.push(node);
				}
			}
		}
	}
	return false;
}


int main() {
	
	cin >> n >> m;
	vector<vector<char>> maze(n, vector<char>(m,'\0'));
	ii start, end;

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cin >> maze[i][j];
			if (maze[i][j] == 'A') start = mp(i,j);
			else if (maze[i][j] == 'B') end = mp(i,j);
		}
	}


	vector<vector<int>> prevStep(n, vector<int>(m,'\0'));

	if (bfs(maze,prevStep,start,end)) {
		cout << "YES\n";
		string path = getPath(prevStep,start,end);
		cout << path.size() << '\n' << path << '\n';
	} else {
		cout << "NO\n";
	}

}
