from manimanims.extra_code.graph_functions import myGraph

vertices = [i + 1 for i in range(6)]
edges = [[(i+1)%5+1] for i in range(6)]
print(edges)
g = myGraph(vertices=vertices, edges=edges)
