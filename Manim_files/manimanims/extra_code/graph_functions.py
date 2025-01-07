"""
This file contains a word by word copy of manim-weighted-line, as it's not
mantained for Python >3.12, and so I'm not able to use it on this project as
a module. If it could be done, I'd have done so, but I already did all of this
project in the most recent version of both Python and Manim at the time, and
I'm not ready for the possible problems that could come from this change.
"""
from __future__ import annotations
from typing import Literal, Hashable, Any
from copy import copy

from manim import config, tempconfig
from manim.animation.creation import Create
from manim.constants import DEFAULT_FONT_SIZE, ITALIC, SMALL_BUFF
from manim.mobject.graph import DiGraph, Graph
from manim.mobject.geometry.line import Line
from manim.mobject.geometry.arc import Dot
from manim.mobject.text.text_mobject import Text
from manim.scene.scene import Scene
from manim.utils.color import ManimColor, RED, BLUE, GREEN

from . import my_configurations as gc


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
            "color": config.background_color, # This is mine
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
        vertices = [i+1 for i in range(5)]
        edges=[
            [2,3,4],
            [1,3,5],
            [1,2,4],
            [1,3],
            [2]
        ]

        self.g1 = myGraph(
            vertices=vertices,
            edges=edges
        )

        edges = [
            [(j, (j+1)**2 if i < j else (i+1)**2) for j in edges[i-1]] for i in vertices
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
        self.algorithm(1)
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
    def __init__(
            self, 
            vertices, 
            edges, 
            labels = gc.labels, 
            label_fill_color = gc.label_fill_colour, 
            layout = gc.layout, 
            layout_scale = gc.layout_scale,
            layout_config = gc.layout_config, 
            vertex_type = gc.vertex_type, 
            vertex_config = gc.vertex_config, 
            vertex_mobjects = {}, 
            edge_type = gc.edge_type,
            partitions = gc.partitions, 
            root_vertex = gc.root_vertex, 
            edge_config = {}
        ):
        # Adjacency list
        self.adj = edges

        # Edge admin
        edges, weights = edge_list(edges)

        # Edge configuration update
        econfig = copy(gc.edge_config)
        econfig.update(edge_config)

        default_econfig = {k: v for k,v in econfig.items() if not isinstance(k, tuple)}
        edge_config = {k: copy(default_econfig) for k in edges}
        for k in edges:
            if k in econfig:
                edge_config.update(econfig[k])
        if weights:
            edge_type = WeightedLine
            for k in edges:
                edge_config[k]["weight"] = weights[k]

        # Vertex configuration update
        vconfig = copy(gc.vertex_config)
        vconfig.update(vertex_config)

        default_vconfig = {k: v for k, v in vconfig.items() if k not in vertices}
        vertex_config = {k: copy(default_vconfig) for k in vertices}

        # For subgraph and other functions
        self.gc = {
            "vertices": vertices, 
            "edges": edges, 
            "labels": labels, 
            "label_fill_color": label_fill_color, 
            "layout": layout, 
            "layout_scale": layout_scale,
            "layout_config": layout_config, 
            "vertex_type": vertex_type, 
            "vertex_config": vertex_config, 
            "vertex_mobjects": vertex_mobjects, 
            "edge_type": edge_type,
            "partitions": partitions, 
            "root_vertex": root_vertex, 
            "edge_config": edge_config
        }

        edge_config.update(econfig)
        vertex_config.update(vconfig)

        super().__init__(
            vertices, 
            edges, 
            labels, 
            label_fill_color, 
            layout, 
            layout_scale, 
            layout_config, 
            vertex_type, 
            vertex_config, 
            vertex_mobjects, 
            edge_type, 
            partitions, 
            root_vertex, 
            edge_config
        )


    def subgraph(self, vertices=list[int]) -> myGraph:
        """Returns a subgraph with specified vertices"""
        outgraph=self.__class__(
            **self.gc
        )
        outgraph.remove_vertices(
            *[v for v in outgraph.vertices if v not in vertices]
        )
        return outgraph


    def _populate_edge_dict(
        self, edges: list[tuple[Hashable, Hashable]], edge_type: type[Line]
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
    def __init__(
            self, 
            vertices, 
            edges, 
            labels = gc.labels, 
            label_fill_color = gc.label_fill_colour, 
            layout = gc.layout, 
            layout_scale = gc.layout_scale,
            layout_config = gc.layout_config, 
            vertex_type = gc.vertex_type, 
            vertex_config = gc.vertex_config, 
            vertex_mobjects = {}, 
            edge_type = gc.edge_type,
            partitions = gc.partitions, 
            root_vertex = gc.root_vertex, 
            edge_config = {}
        ):
        # Adjacency list
        self.adj = edges

        # Edge admin
        edges, weights = edge_list(edges)

        # Edge configuration update
        econfig = copy(gc.edge_config)
        econfig.update(edge_config)

        default_econfig = {k: v for k,v in econfig.items() if not isinstance(k, tuple)}
        edge_config = {k: copy(default_econfig) for k in edges}
        for k in edges:
            if k in econfig:
                edge_config.update(econfig[k])
        if weights:
            edge_type = WeightedLine
            for k in edges:
                edge_config[k]["weight"] = weights[k]

        # Vertex configuration update
        vconfig = copy(gc.vertex_config)
        vconfig.update(vertex_config)

        default_vconfig = {k: v for k, v in vconfig.items() if k not in vertices}
        vertex_config = {k: copy(default_vconfig) for k in vertices}

        # For subgraph and other functions
        self.gc = {
            "vertices": vertices, 
            "edges": edges, 
            "labels": labels, 
            "label_fill_color": label_fill_color, 
            "layout": layout, 
            "layout_scale": layout_scale,
            "layout_config": layout_config, 
            "vertex_type": vertex_type, 
            "vertex_config": vertex_config, 
            "vertex_mobjects": vertex_mobjects, 
            "edge_type": edge_type,
            "partitions": partitions, 
            "root_vertex": root_vertex, 
            "edge_config": edge_config
        }

        edge_config.update(econfig)
        vertex_config.update(vconfig)

        super().__init__(
            vertices, 
            edges, 
            labels, 
            label_fill_color, 
            layout, 
            layout_scale, 
            layout_config, 
            vertex_type, 
            vertex_config, 
            vertex_mobjects, 
            edge_type, 
            partitions, 
            root_vertex, 
            edge_config
        )


    def subgraph(self, vertices=list[int]) -> myGraph:
        """Returns a subgraph with specified vertices"""
        outgraph=self.__class__(
            **self.gc
        )
        outgraph.remove_vertices(
            *[v for v in outgraph.vertices if v not in vertices]
        )
        return outgraph


    def _populate_edge_dict(
        self, edges: list[tuple[Hashable, Hashable]], edge_type: type[Line]
    ):
        self.edges = {
            (u, v): edge_type(
                self[u],
                self[v],
                z_index=-2,
                **self._edge_config[(u, v)],
            )
            for (u, v) in edges
        }

        for (u, v), edge in self.edges.items():
            edge.add_tip(**self._tip_config[(u, v)])


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
    if not adj:
        return ([], {})
    if type(adj[0][0]) == int:
        if directed:
            edges = [(i+1, v) for i in range(len(adj)) for v in adj[i]]
        else:
            # Important: This notation permits introducing an adjacency list as
            # if it was expressing a directed graph, but introducing one 
            # expressing an undirected one also works, meaning omiting the
            # vertex in the adjacency from the larger numbered vertex-
            edges = [(i+1, v) for i in range(len(adj)) for v in adj[i] if i <= v]
        return (edges, {})
    if directed:
        edges = [
            ((i+1, v[0]), v[1]) for i in range(len(adj)) for v in adj[i]
        ]
    else:
        edges = [
            ((i+1, v[0]), v[1]) 
            for i in range(len(adj)) 
            for v in adj[i] if i <= v[0]
        ]
    return ([e[0] for e in edges], {e[0]: e[1] for e in edges})


def dict_update(dct: dict, update: dict):
    for key in update.keys():
        if update[key]:
            if isinstance(update[key], dict):
                dct[key] = dct.get(key, {})
                dict_update(dct[key], update[key])
            else:
                dct[key] = update[key]
