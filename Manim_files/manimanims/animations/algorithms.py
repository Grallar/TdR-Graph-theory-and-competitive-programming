import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

from extra_code.graph_functions import (
    myGraph, myDiGraph, GraphScene, render_all, WeightedLine
)
from extra_code.my_configurations import graph_configuration
from manim import *
from math import sin, cos, pi, inf
from queue import PriorityQueue
from copy import copy

class DFS(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = [False] * len(self.g1.myvertices)

    def algorithm(self, v):
        self.seen[v] = True
        self.v_act(v+1, self.g1, self.v_processing_colour)

        for u in self.g1.myedges[v]:
            if self.seen[u]:
                continue
            edge = (v+1, u+1)
            self.wait()
            self.e_act(edge, self.g1, self.e_visited_colour)
            self.v_act(v+1, self.g1, self.v_visited_colour)
            self.algorithm(u)
            self.e_act(
                edge, self.g1, self.e_processed_colour, True
            )
            self.v_act(v+1, self.g1, self.v_processing_colour)
        self.v_act(v+1, self.g1, self.v_processed_colour)
    

class BFS(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = [False] * len(self.g1.myvertices)
        self.q = []

    def algorithm(self, v):
        self.q.append(v)
        self.seen[v] = True

        while self.q:
            a = self.q.pop(0)
            self.v_act(a+1, self.g1, self.v_processing_colour)
            for b in self.g1.myedges[a]:
                if self.seen[b]:
                    continue
                edge = (a+1, b+1)
                self.e_act(edge, self.g1, self.e_visited_colour)
                self.wait(0.5)
                self.v_act(b+1, self.g1, self.v_visited_colour)
                self.seen[b] = True
                self.q.append(b)
            self.wait(0.5)
            self.v_act(a+1, self.g1, self.v_processed_colour)


class BellmanFord(GraphScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g1 = self.wg1
    
    def algorithm(self, v):
        # MUST ALSO PUT THE LIST OF DISTANCES, MAYBE UNDER? SHOULD BE SEEN, SO ERPVQPUWEBVUQIWBEPNQUWECRQPWCQUINECQONWUEROQNWCRPOQW
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
        # MUST ALSO PUT THE LIST OF DISTANCES, MAYBE UNDER? SHOULD BE SEEN, SO ERPVQPUWEBVUQIWBEPNQUWECRQPWCQUINECQONWUEROQNWCRPOQW
        dist = [inf] * len(self.g1.vertices)
        dist[v] = 0
        self.q.append(v)

        while self.q:
            a = self.q.pop(0)
            self.v_act(a+1, self.g1, self.v_processing_colour)

            for b, w in self.g1.myedges[a]:
                e = (a+1, b+1) if a < b else (b+1,a+1)
                returning = False if a < b else True
                self.e_act(e, self.g1, self.e_processing_colour, returning)

                if dist[b] > dist[a] + w:
                    self.e_act(e, self.g1, self.e_processed_colour, returning)
                    dist[b] = dist[a] + w

                    if not b in self.q:
                        self.q.append(b)
                
                self.e_act(e, self.g1, self.e_visited_colour, returning)
            self.v_act(a+1, self.g1, self.v_visited_colour)


class Dijkstra(GraphScene):
    scene_temp_config = {
        "frame_size": (1000, 800),
        "frame_width": 5,
        "frame_height": 4
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g1 = self.wg1
        self.g1.move_to([-2, 0, 0])
        self.q = PriorityQueue()

    def algorithm(self, v):
        seen = [False] * len(self.g1.vertices)
        distancia = [inf] * len(self.g1.vertices)
        distancia[v] = 0
        self.q.put((distancia[v], v))
        while  self.q.qsize() != 0:
            a = self.q.get()[1]
            if seen[a]:
                continue
            seen[a] = True
            self.v_act(a+1, self.g1, self.v_visited_colour)
            for b, w in self.g1.myedges[a]:
                edge = (a+1,b+1) if a < b else (b+1,a+1)
                returning = False if a < b else True
                self.e_act(edge, self.g1, self.e_processing_colour, returning)
                if distancia[a] + w < distancia[b]:
                    self.e_act(edge, self.g1, self.e_processed_colour, returning)
                    distancia[b] = distancia[a] + w
                    self.q.put((distancia[b], b))
                self.e_act(edge, self.g1, self.e_visited_colour, returning)


class FloydWarshall(BellmanFord):

    def algorithm(self, v):
        edges = [
            [e[0] for e in self.g1.myedges[i]]
            for i in range(len(self.g1.vertices))
        ]
        distancia = [
            [
                0 if i == j
                else self.g1.myedges[i][edges[i].index(j)][1] if j in edges[i]
                else inf
                for j in range(len(self.g1.vertices))
            ] 
            for i in range(len(self.g1.vertices))
        ]
        paths = [
            [
                None if i == j
                else [j] if distancia[i][j] < inf
                else None
                for j in range(len(self.g1.vertices))
            ]
            for i in range(len(self.g1.vertices))
        ]
        for v in range(len(self.g1.vertices)):
            self.v_act(v+1, self.g1, self.v_processing_colour)
            self.wait()
            for i in range(len(self.g1.vertices)):
                for j in range(len(self.g1.vertices)):
                    if i != j and i != v and j != v:
                        path_ij = copy(paths[i][j])
                        path_iv = copy(paths[i][v])
                        path_vj = copy(paths[v][j])
                        if path_iv and path_vj:
                            path_v = copy(paths[i][v] + paths[v][j])
                        else:
                            path_v = None
                        print(path_ij, path_v)
                        print(i, j, v)
                        self.es_act(i, path_ij, self.g1, self.e_processing_colour)
                        self.es_act(i, path_v, self.g1, self.e_visited_colour)
                        self.wait(0.5)
                        if distancia[i][v] + distancia[v][j] < distancia[i][j]:
                            distancia[i][j] = copy(distancia[i][v] + distancia[v][j])
                            paths[i][j] = copy(path_v)
                        self.es_act(i, paths[i][j], self.g1, self.e_processed_colour)
                        self.wait(0.5)
                        self.es_act(i, path_ij, self.g1, config.background_color.invert())
                        self.es_act(i, path_v, self.g1, config.background_color.invert())
                    elif i == v:
                        pass
                    elif j == v:
                        pass
                    else:           #Vertexs iguals
                        pass

            self.wait()
            self.v_act(v+1, self.g1, config.background_color.invert())
            for path in paths:
                print(path)
    
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
    to_render = [DFS, BFS, BellmanFord, SPFA, Dijkstra, FloydWarshall]

    render_all(to_render, name_prefix)