import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

from extra_code.graph_functions import (
    myGraph, myDiGraph, GraphScene, render_all
)
from manim import *
from math import inf
from queue import PriorityQueue

class DFS(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = [False] * len(self.g1.vertices)
    
    def construct(self):
        self.play(Create(self.g1))
        self.algorithm(1)
        self.wait(1)

    def algorithm(self, v):
        self.seen[v-1] = True
        self.v_act(v, self.g1, self.v_processing_colour)

        for u in self.g1.adj[v-1]:
            if self.seen[u-1]:
                continue
            edge = (v, u)
            self.wait()
            self.e_act(edge, self.g1, self.e_visited_colour)
            self.v_act(v, self.g1, self.v_visited_colour)
            self.algorithm(u)
            self.e_act(
                edge, self.g1, self.e_processed_colour, True
            )
            self.v_act(v, self.g1, self.v_processing_colour)
        self.v_act(v, self.g1, self.v_processed_colour)
    

class BFS(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = [False] * len(self.g1.vertices)
        self.q = []
    
    def algorithm(self, v):
        self.q.append(v)
        self.seen[v-1] = True

        while self.q:
            a = self.q.pop(0)
            self.v_act(a, self.g1, self.v_processing_colour)
            for b in self.g1.adj[a-1]:
                if self.seen[b-1]: 
                    continue 
                edge = (a, b)
                self.e_act(edge, self.g1, self.e_visited_colour)
                self.wait(0.5)
                self.v_act(b, self.g1, self.v_visited_colour)
                self.seen[b-1] = True
                self.q.append(b)
            self.wait(0.5)
            self.v_act(a, self.g1, self.v_processed_colour)
            print(self.q)


class BellmanFord(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g1 = self.wg1
    
    def algorithm(self, v):
        dist = [inf] * len(self.g1.vertices)
        dist[v] = 0
        edges = [
            (e[0]-1, e[1]-1, self.g1._edge_config[e]["weight"])
            for e in self.g1.edges
        ]

        for _ in range(len(self.g1.vertices)):
            for e in edges:
                a, b, w = e
                edge = (a+1,b+1)
                self.e_act(edge, self.g1, self.e_processing_colour)
                self.wait(0.5)
                if dist[a] + w < dist[b]:
                    dist[b] = dist[a] + w
                    self.e_act(edge, self.g1, self.e_processed_colour)
                self.wait()
                self.e_act(edge, self.g1, self.e_visited_colour)
    
    def e_act(
        self,
        e: tuple[int, int],
        graph: myGraph | myDiGraph,
        colour: ManimColor
    ):
        typ: type[Line] = graph.gc["edge_type"]
        kwargs = graph._edge_config[e]
        kwargs["color"] = colour
        coor = {
            "start": graph[e[0]].get_center(),
            "end": graph[e[1]].get_center()
        }
        edge = typ(z_index=-1, **coor, **kwargs)
        self.remove(graph.edges[e])
        self.add(edge)
        graph.edges[e] = edge


class SPFA(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g1 = self.wg1
        self.q = []
    
    def algorithm(self, v):
        dist = [inf] * len(self.g1.vertices)
        dist[v-1] = 0
        self.q.append(v)

        while self.q:
            a = self.q.pop(0)
            self.v_act(a, self.g1, self.v_processing_colour)

            for b, w in self.g1.adj[a-1]:
                e = (a, b) if a < b else (b, a)
                returning = a > b 
                self.e_act(e, self.g1, self.e_processing_colour, returning)

                if dist[b-1] > dist[a-1] + w:
                    self.e_act(e, self.g1, self.e_processed_colour, returning)
                    dist[b-1] = dist[a-1] + w

                    if not b in self.q:
                        self.q.append(b)
                
                self.e_act(e, self.g1, self.e_visited_colour, returning)
            self.v_act(a, self.g1, self.v_visited_colour)


class Dijkstra(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g1 = self.wg1
        self.q = PriorityQueue()

    def algorithm(self, v):
        seen = [False] * len(self.g1.vertices)
        distancia = [inf] * len(self.g1.vertices)
        distancia[v-1] = 0
        self.q.put((distancia[v-1], v))
        while self.q.qsize() != 0:
            a = self.q.get()[1]
            if seen[a-1]:
                continue
            seen[a-1] = True
            self.v_act(a, self.g1, self.v_visited_colour)
            for b, w in self.g1.adj[a-1]:
                edge = (a,b) if a < b else (b,a)
                returning = a > b
                self.e_act(edge, self.g1, self.e_processing_colour, returning)
                if distancia[a-1] + w < distancia[b-1]:
                    self.e_act(edge, self.g1, self.e_processed_colour, returning)
                    distancia[b-1] = distancia[a-1] + w
                    self.q.put((distancia[b-1], b))
                self.e_act(edge, self.g1, self.e_visited_colour, returning)


class FloydWarshall(BellmanFord):
    def algorithm(self, v):
        edges = [
            [e[0] for e in self.g1.adj[i]]
            for i in range(len(self.g1.vertices))
        ]
        distancia = [
            [
                0 if i == j
                else self.g1.adj[i][edges[i].index(j+1)][1] if j+1 in edges[i]
                else inf
                for j in range(len(self.g1.vertices))
            ] 
            for i in range(len(self.g1.vertices))
        ]
        for v in self.g1.vertices:
            for i in self.g1.vertices:
                for j in self.g1.vertices:
                    self.v_act(v, self.g1, self.v_processing_colour)
                    self.v_act(i, self.g1, self.v_visited_colour)
                    self.v_act(j, self.g1, self.v_visited_colour)
                    self.wait()
                    if distancia[i-1][v-1] + distancia[v-1][j-1] < distancia[i-1][j-1]:
                        distancia[i-1][j-1] = distancia[i-1][v-1] + distancia[v-1][j-1]
                        self.v_act(v, self.g1, self.v_processed_colour)
                        self.wait(0.5)
                        self.v_act(v, self.g1, self.v_processing_colour)
                    else:
                        self.v_act(i, self.g1, self.v_processed_colour)
                        self.v_act(j, self.g1, self.v_processed_colour)
                        self.wait(0.5)
                        self.v_act(i, self.g1, self.v_visited_colour)
                    self.v_act(j, self.g1, config.background_color.invert())
                    self.v_act(i, self.g1, config.background_color.invert())
                    self.v_act(v+1, self.g1, config.background_color.invert())
    
    def es_act(
        self, v: int, path: list[int], graph: myGraph | myDiGraph, colour: ManimColor
    ):
        if path is None or path == []:
            return
        self.e_act((v+1, path[0]+1) if v < path[0] else (path[0]+1, v+1), graph, colour)
        for i in range(len(path)-1):
            edge = (path[i]+1, path[i+1]+1) if path[i] < path[i+1] else (path[i+1]+1, path[i]+1)
            self.e_act(edge, graph, colour)




if __name__ == "__main__":
    name_prefix = "alg"
    to_render = [
        (DFS, "DFS"),
        (BFS, "BFS"), 
        (BellmanFord, "BellmanFord"),
        (SPFA, "SPFA"), 
        (Dijkstra, "Dijkstra"), 
        (FloydWarshall, "FloydWarshall")
    ]

    render_all(to_render, name_prefix)