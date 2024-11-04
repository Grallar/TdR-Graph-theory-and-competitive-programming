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
from math import sin, cos, pi


class Graph1(GraphScene): # Graph example
    def construct(self):
        g1 = myGraph(
            vertices=[i for i in range(7)],
            edges=[[j for j in range(7)] for _ in range(7)]
        )

        self.add(g1)


class Graph2(GraphScene): # Graph example
    def construct(self):
        g1 = myGraph(
            vertices=[i for i in range(5)],
            edges=[[i] for i in range(1,5)]
        )

        self.add(g1)


class Graph3(GraphScene): # Subgraph example
    scene_temp_config = {
        "frame_width": 12,
        "frame_height": 8,
        "pixel_width": 1200,
        "pixel_height": 800
    }

    def construct(self):
        g1 = myGraph(
            vertices=[i for i in range(6)],
            edges=[[2,3],[2,4],[0,1,3],[0,2,4],[1,3]]
        )
        subg1 = g1.subgraph([i for i in range(4)])

        g1.move_to([-3, 0, 0])
        subg1.move_to([3, 0, 0])
        self.add(g1, subg1)


class Graph4(GraphScene): # Loop example
    def construct(self):
        g1 = myGraph(
            vertices=[i for i in range(5)],
            edges=[[i,i+1] for i in range(4)] + [[4]]
        )
        """centers = [
            Vector()
        ]
        loops = [
            Circle(
                g1.vertices[i].arc_center,
                g1.vertices[i].arc_center,
                color=BLACK,
                radius=1,
                arc_center=
            )
            for i in range(1,5)
        ]"""
        self.add(g1)


class Graph5(GraphScene): # Parallel edge example
    def construct(self):
        g1 = Graph(
            vertices=[i+1 for i in range(6)],
            edges=[(1,2),(2,1)],
            **graph_configuration
        )
        self.add(g1)


class Graph6(GraphScene): # Isomorphism example
    scene_temp_config = {
        "frame_width": 12,
        "frame_height": 8,
        "pixel_width": 1200,
        "pixel_height": 800
    }

    def construct(self):
        g1 = myGraph(
            vertices=[i for i in range(4)],
            edges=[[j for j in range(i+1,4)] for i in range(4)]
        )
        g2 = g1.subgraph(g1.myvertices)
        
        g1.move_to([-3, 0, 0])
        g2.move_to([3, 0, 0])
        for i in range(3):
            g2.vertices[i+1].move_to([3+2*sin(i*2*pi/3), 2*cos(i*2*pi/3), 0])
        g2[4].move_to([3, 0, 0])
        g2.update_edges(g2)

        self.add(g1, g2)


class Graph7(GraphScene): # Weighted graph example
    def construct(self):
        g1 = myGraph(
            vertices=[i for i in range(6)],
            edges=[[(i+1, i+1)] for i in range(5)],
            edge_type=WeightedLine,
        )

        self.add(g1)


class Graph8(GraphScene): # Directed graph example
    def construct(self):
        g1 = myDiGraph(
            vertices=[i for i in range(10)],
            edges=[[(i+1)%10, (i+4)%10] for i in range(10)]
        )

        self.add(g1)


if __name__ == "__main__":
    name_prefix = "3_2"
    graphs: list[type[myGraph]] = [
        Graph1, Graph2, Graph3, Graph4, Graph5, Graph6, Graph7, Graph8
    ]

    render_all(graphs, name_prefix)
