from math import inf
from queue import PriorityQueue


def dfs(adj: list[list[int]], start_vertex: int):
    """adj: llista d'adjacencia; start_vertex: vertex inicial"""
    visitat = [False for _ in adj]

    def dfs_rec(a):
        visitat[a] = True
        for b in adj[a]:
            if visitat[b]:
                continue
            # Codi
            dfs_rec(b)

    dfs_rec(start_vertex)


def bfs(adj: list[list[int]], start_vertex: int):
    """adj: llista d'adjacencia; start_vertex: vertex inicial"""
    cua = []
    visitat = [False for _ in adj]
    cua.append(start_vertex)
    visitat[start_vertex] = True

    while cua:
        a = cua.pop(0)
        for b in adj[a]:
            if visitat[b]:
                continue
            visitat[b] = True
            # Codi
            cua.append(b)


def bllfrd(
    v_num: int,
    edges: list[tuple[int, int, int]],
    start_vertex: int,
):
    """
    v_num: nombre de vertexs; edges: llista d'arestes en format
    (inicial, final, pes); start_vertex: vertex inicial
    """
    dist = [inf for _ in range(v_num)]
    dist[start_vertex] = 0

    for _ in range(v_num):
        for e in edges:
            a, b, w = e
            dist[b] = min(dist[b], dist[a] + w)


def spfa(adj: list[list[tuple[int, int]]], start_vertex: int):
    """
    adj: llista d'adjacencia amb tuples (v, w) on v: vertex, w: pes de l'aresta
    que connecta; start_vertex: vertex inicial
    """
    cua = [start_vertex]
    dist = [inf for _ in adj]
    encua = [False for _ in adj]
    dist[start_vertex] = 0

    while cua:
        a = cua.pop(0)
        encua[a] = False

        for b, w in adj[a]:
            if dist[b] > dist[a] + w:
                dist[b] = dist[a] + w

                if not encua[b]:
                    cua.append(b)
                    encua[b] = True


def dijkstra(adj: list[list[tuple[int, int]]], start_vertex):
    """
    adj: llista d'adjacencia amb tuples (v, w) on v: vertex, w: pes de l'aresta
    que connecta; start_vertex: vertex inicial
    """
    cua = PriorityQueue()
    visitat = [False for _ in adj]
    distancia = [inf for _ in adj]
    distancia[start_vertex] = 0
    cua.put((distancia[start_vertex], start_vertex))
    while cua.qsize() != 0:
        a = cua.get()[1]
        if visitat[a]:
            continue
        visitat[a] = True
        for b, w in adj[a]:
            if distancia[a] + w < distancia[b]:
                distancia[b] = distancia[a] + w
                cua.put((distancia[b], b))


def fldwrshll(adj: list[list[int]]):
    """
    adj: matriu d'adjacencia amb valors corresponents al pes l'aresta que
    connecta els vertexs
    """
    distancia = [
        [0 if i == j
         else adj[i][j] if adj[i][j]
         else inf
         for j in range(len(adj))]
        for i in range(len(adj))
    ]
    for v in range(len(adj)):
        for i in range(len(adj)):
            for j in range(len(adj)):
                distancia[i][j] = min(
                    distancia[i][j], distancia[i][v] + distancia[v][j]
                )


"""class UnionFindStructure:
    def __init__(self, size):
        self.predecessor = [i for i in range(size)]
        self.size = [1] * size
    
    def find(self, v):
        pass
"""

def toposort(adj: list[list[int]]):
    """
    adj: llista d'adjacencia
    """
    second_state = [False for _ in adj]
    first_state = [False for _ in adj]
    processed = []

    def dfs(v: int):
        if first_state[v]:
            raise TypeError(f"Graph has a cycle in it, should be acyclical")
        if second_state[v]: 
            return
        first_state[v] = True
        for u in adj[v]:
            dfs(u)
        first_state[v] = False
        second_state[v] = True
        processed.append(v)

    for i in range(len(adj)):
        # Si s'aplica diverses vegades, es que hi ha components als 
        # que no es pot arribar des del vertex inicial
        dfs(i)

    return processed[::-1]

dijkstra([[(1,1),(2,3)], [(0,1),(2,1)], [(0, 3),(1,1)]], 2)