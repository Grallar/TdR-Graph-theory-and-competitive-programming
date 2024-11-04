"""
This file contains a word by word copy of manim-weighted-line, as it's not
mantained for Python >3.12, and so I'm not able to use it on this project as
a module. If it could be done, I'd have done so, but I already did all of this
project in the most recent version of both Python and Manim at the time, and
I'm not ready for the possible problems that could come from this change.
"""
from __future__ import annotations
from typing import Literal, Hashable

from manim import config, tempconfig
from manim.animation.creation import Create
from manim.mobject.graph import DiGraph, Graph
from manim.scene.scene import  Scene
from manim.constants import DEFAULT_FONT_SIZE, ITALIC, SMALL_BUFF
from manim.mobject.mobject import Mobject
from manim.mobject.geometry.line import Line
from manim.mobject.geometry.arc import Dot, LabeledDot
from manim.mobject.text.text_mobject import Text
from manim.mobject.text.tex_mobject import MathTex
from manim.utils.color import ManimColor, RED, BLUE, GREEN

from .my_configurations import graph_configuration as gc

from typing import Any
from copy import copy


type EdgeList = list[tuple[int, int]]
type Adj = list[list[int]]
type wAdj = list[list[tuple[int, int]]]

"""
The following class is a copy, except for the weight_config["color"] part, of
the manim-weighted-line module, which isn't usable in this version of Manim
"""
class WeightedLine(Line):
    """A line to display weighted edges in a network graph.

    Parameters
    ----------
    args
        Arguments to be passed to :class:`Line`
    weight
        The weight of the edge to display
    weight_config
        Dict of options to be passed to :class:`Text`
    weight_alpha
        The alpha position on the edge to show the weight
    bg_config
        Dict of options to be passed to :class:`Rectangle`
    add_bg
        Boolean to show a rectangle behind the weight
    kwargs
        Additional arguments to be passed to :class:`Line`

    """

    def __init__(
        self,
        *args: Any,
        weight: str | int | float | None = None,
        weight_config: dict | None = None,
        weight_alpha: float = 0.5,
        bg_config: dict | None = None,
        add_bg: bool = True,
        **kwargs: Any,
    ):
        self.weight = weight
        self.alpha = weight_alpha
        self.add_bg = add_bg
        super().__init__(*args, **kwargs)

        self.weight_config = {
            "color": config.background_color.invert(),
            "slant": ITALIC,
            "font_size": DEFAULT_FONT_SIZE * 0.5,
        }

        if weight_config:
            self.weight_config.update(weight_config)

        self.bg_config = {
            "color": config.background_color,
            "opacity": 1,
        }
        if bg_config:
            self.bg_config.update(bg_config)

        if self.weight is not None:
            self._add_weight()

    def _add_weight(self):
        """
        Clears any current weight and then displays the weight is not none.

        Use weight_config dict to send options to the Text object.

        Use bg_config dict to send options to the background Rectangle object.

        """

        # Set the new weight if it is present

        point = self.point_from_proportion(self.alpha)
        label = Text(str(self.weight), **self.weight_config)
        label.move_to(point)

        if self.add_bg:
            label.add_background_rectangle(**self.bg_config)
            label.background_rectangle.height += SMALL_BUFF

        self.add(label)


class GraphScene(Scene):
    scene_temp_config: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vertices = [i for i in range(5)]
        edges=[
            [1,2,3],
            [0,2,4],
            [0,1,3],
            [0,2],
            [1]
        ]

        self.g1 = myGraph(
            vertices=vertices,
            edges=edges
        )

        edges = [
            [(j, (j+1)**2 if i < j else (i+1)**2) for j in edges[i]] for i in range(len(edges))
        ]

        self.wg1 = myGraph(
            vertices=vertices,
            edges=edges
        )
        self.v_visited_colour = RED
        self.v_processing_colour = BLUE
        self.v_processed_colour = GREEN
        self.e_visited_colour = RED
        self.e_processing_colour = BLUE
        self.e_processed_colour = GREEN


    def construct(self):
        self.play(Create(self.g1))
        self.algorithm(0)
        self.wait(1)
    
    def algorithm(self, v):
        raise NotImplementedError("Should be done in subclasses")

    def e_act(
        self,
        e: tuple[int, int],
        graph: myGraph | myDiGraph,
        colour: ManimColor,
        returning: bool = False
    ):
        """Remember that edge should be (v+1, u+1)"""
        typ: type[Line] = graph.gc["edge_type"]
        kwargs = graph._edge_config[e]
        kwargs["color"] = colour
        coor = {
            "start": graph[e[0]].get_center(),
            "end": graph[e[1]].get_center()
        }
        edge = typ(z_index=-1, **coor, **kwargs)
        if returning:
            self.play(Create(edge.reverse_direction())) # Del vèrtex u al v
        else:
            self.play(Create(edge)) # Del vèrtex v a l'u
        graph.edges[e] = edge
    
    def v_act(
        self, v: int, graph: myGraph | myDiGraph, colour: ManimColor
    ):
        """Remember """
        typ: type[Dot] = graph.gc["vertex_type"]
        kwargs = graph._vertex_config[v]
        kwargs["color"] = colour
        coor = {
            "point": graph[v].get_center()
        }
        vertex = typ(**coor, **kwargs)
        self.add(vertex)
        self.remove(graph[v])


class myGraph(Graph):
    def __init__(self, *args, vertices, edges: Adj | wAdj, **kwargs):
        self.args = args
        self.kwargs = copy(kwargs)
        self.gc = copy(kwargs)
        for key in gc.keys():
            if isinstance(gc[key], dict):
                self.gc[key] = self.gc.get(key, {})
                self.gc[key].update(gc[key])
            else:
                self.gc[key] = gc[key]

        """
        The next section of code manages the edges and vertices.
        """
        self.gc["vertices"] = [v+1 for v in vertices]
        new_edges = edge_list(edges)
        self.gc["edges"] = new_edges[0]

        """
        Manim's base class for graphs, GenericGraph, in the case of specific
        configurations for the edges, uses that specific configuration and
        foregoes the general one, which isn't how it's done in this project.
        The next section of the code copies the general configuration into
        each edge's specific one. In the case of weighted edges, it adds their
        weight as a specific parameter. 
        """
        if "edge_config" in self.gc.keys():
            my_default_edge_config = {
                k: v
                for k, v in self.gc["edge_config"].items()
                if not isinstance(k, tuple)
            }
        else:
            my_default_edge_config: dict = {}
        my_edge_config = {e: copy(my_default_edge_config) for e in self.gc["edges"]}

        for e in self.gc["edges"]:
            if e in self.gc["edge_config"].keys():
                my_edge_config.update(self.gc["edge_config"][e])
        self.gc["edge_config"] = copy(my_edge_config)

        if new_edges[1]:
            self.gc["edge_type"] = WeightedLine
            for key in new_edges[1].keys():
                self.gc["edge_config"][key].update(new_edges[1][key])
        
        if "vertex_config" in self.gc.keys():
            my_default_vertex_config = {
                k: v for k, v in self.gc["vertex_config"].items() if k not in vertices
            }
        else:
            my_default_vertex_config = {}
        my_vertex_config = {
            v: copy(my_default_vertex_config) for v in vertices
        }
        for v in self.gc["vertices"]:
            if v in self.gc["vertex_config"].keys():
                my_vertex_config.update(self.gc["vertex_config"])

        self.gc["edge_type"] = self.gc.get("edge_type", Line)
        self.gc["vertex_type"] = self.gc.get("vertex_type", Dot)
        
        if "labels" in self.gc.keys() and self.gc["vertex_type"] == Dot:
            self.gc["vertex_type"] = LabeledDot

        super().__init__(*args, **self.gc)
        self.gc.pop("vertices")
        self.gc.pop("edges")
        self.myvertices = vertices
        self.myedges = edges
    
    def subgraph(self, vertices=list[int]) -> myGraph:
        """Returns a subgraph with specified vertices"""
        outgraph=self.__class__(
            *self.args, 
            vertices=self.myvertices, 
            edges=self.myedges, 
            **self.kwargs
        )
        outgraph.remove_vertices(
            *[v for v in outgraph.vertices if v-1 not in vertices]
        )
        return outgraph

    def _populate_edge_dict(
        self, edges: list[tuple[Hashable, Hashable]], edge_type: type[Mobject]
    ):
        self.edges = {
            (u, v): edge_type(
                self[u].get_center(),
                self[v].get_center(),
                z_index=-2,
                **self._edge_config[(u, v)],
            )
            for (u, v) in edges
        }



class myDiGraph(DiGraph):
    def __init__(self, *args, vertices, edges: Adj | wAdj, **kwargs):
        self.args = args
        self.kwargs = copy(kwargs)
        self.gc = copy(kwargs)
        for key in gc.keys():
            if isinstance(gc[key], dict):
                self.gc[key] = self.gc.get(key, {})
                self.gc[key].update(gc[key])
            else:
                self.gc[key] = gc[key]

        """
        The next section of code manages the edges and vertices.
        """
        self.gc["vertices"] = [v+1 for v in vertices]
        new_edges = edge_list(edges, True)
        self.gc["edges"] = new_edges[0]

        """
        Manim's base class for graphs, GenericGraph, in the case of specific
        configurations for the edges, uses that specific configuration and
        foregoes the general one, which isn't how it's done in this project.
        The next section of the code copies the general configuration into
        each edge's specific one, with the exception of "tip_config", which
        is used to determine if an edge will be directed or not, and is
        inputted apart from the rest. In case of weighted edges, it adds their
        weight as a specific parameter. 
        """
        if self.gc["edge_config"]:
            my_default_edge_config = {
                k: v 
                for k, v in self.gc["edge_config"].items() 
                if not isinstance(k, tuple)
            }
            my_edge_config = {k: copy(my_default_edge_config) for k in self.gc["edges"] if isinstance(k, tuple)}
            for e in my_edge_config:
                if e in self.gc["edge_config"].keys():
                    my_edge_config[e].update(self.gc["edge_config"][e])
            self.gc["edge_config"] = my_edge_config

        if new_edges[1]:
            self.gc["edge_type"] = WeightedLine
            for key in new_edges[1].keys():
                self.gc["edge_config"][key] = self.gc["edge_config"].get(key, {})
                self.gc["edge_config"][key].update(new_edges[1][key])

        super().__init__(*args, **self.gc)
        self.gc.pop("vertices")
        self.gc.pop("edges")
        self.myvertices = vertices
        self.myedges = edges
    
    def subgraph(self, vertices=list[int]) -> myDiGraph:
        """Returns a subgraph with specified vertices"""
        outgraph=self.__class__(
            *self.args, vertices=self.myvertices, edges=self.myedges, **self.kwargs
        )
        outgraph.remove_vertices(
            *[v for v in outgraph.vertices if v-1 not in vertices]
        )
        return outgraph



def render_all(
    graphs: list[type[GraphScene]],
    name_prefix: str
) -> Literal[True] | None:
    for i in range(len(graphs)):
        graph: GraphScene = graphs[i]
        with tempconfig(
            {
                "output_file": "g" + name_prefix + "_" + str(i),
                **graph.scene_temp_config
            }
        ):
            graph().render()


def edge_list(
    adj: list[list[int]] | list[list[tuple[int, int]]], directed: bool = False
) -> tuple[EdgeList, dict]:
    """
    Function to turn edges corresponding to indices to edges corresponding
    to values increased by 1. In case of the graph being weighed, it returns
    a dictionary with the corresponding tuples associated to their weight to be
    put into the edge_config of a GenericGraph subclass,
    """
    if type(adj[0][0]) == int:
        if directed:
            edges = [(i+1, v+1) for i in range(len(adj)) for v in adj[i]]
        else:
            # Important: This notation permits introducing an adjacency list as
            # if it was expressing a directed graph, but introducing one 
            # expressing an undirected one also works, meaning omiting the
            # vertex in the adjacency from the larger numbered vertex-
            edges = [(i+1, v+1) for i in range(len(adj)) for v in adj[i] if i <= v]
        return (edges, {})
    if directed:
        edges = [
            ((i+1, v[0]+1), v[1]) for i in range(len(adj)) for v in adj[i]
        ]
    else:
        edges = [
            ((i+1, v[0]+1), v[1]) 
            for i in range(len(adj)) 
            for v in adj[i] if i <= v[0]
        ]
    return ([e[0] for e in edges], {e[0]: {"weight":e[1]} for e in edges})
