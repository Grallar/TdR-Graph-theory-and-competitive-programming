def dfs(i, j, matrix, n, m):
    if not matrix[i][j]:
        return 0
    queue = [(i, j)]
    matrix[i][j] = 0
    while queue:
        a, b = queue.pop(0)
        matrix[a][b] = 0
        for vx, vy in vecs:
            na = a + vx
            mb = b + vy
            if n > na >= 0 and m > mb >= 0 and matrix[na][mb]:
                queue.append((na, mb))
    
def count(matrix, n, m):
    total = 0
    for i in range(n):
        for j in range(m):
            if matrix[i][j]:
                dfs(i,j,matrix,n,m)
                total += 1
 
    return total
 
n, m = map(int, input().split())
matrix = []
total = 0
vecs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for _ in range(n):
    inp = list(input())
    matrix.append([1 if c == "." else 0 for c in inp])
 
print(count(matrix, n, m))