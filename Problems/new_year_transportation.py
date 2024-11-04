n, m = map(int, input().split())
adj = [i+int(j) for (i,j) in zip([i for i in range(n-1)], input().split())]
print([i+1 for i in adj])
def dfs(i):
    if i == m-1:
        return "YES"
    if i == n-1:
        return "NO"
    return dfs(adj[i])

print(dfs(0))